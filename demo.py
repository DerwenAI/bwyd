#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script.
"""

import logging
import pathlib
import sys
import traceback
import typing

from icecream import ic
import jinja2
import requests_cache
import xandergraph as xg

import bwyd


class Corpus:
    """
Manage a corpus of Bwyd modules.
    """

    def __init__ (
        self,
        account: str,
        *,
        config_path: pathlib.Path = pathlib.Path("config.toml"),
        lang: str = "en",
        ) -> None:
        """
Constructor.
        """
        self.lang: str = lang
        self.account: str = account
        self.bwyd_dict: dict[ str, bwyd.Recipe ] = {}

        self.dsl: bwyd.Bwyd = bwyd.Bwyd(
            config_path = config_path,
        )

        self.config = self.dsl.config

        logging.basicConfig(
            format = self.config["bwyd"]["log_format"],
        )

        # init the graph and load the OTTR templates
        self.kg: xg.KnowledgeGraph = xg.KnowledgeGraph(
            ns = {
                "bwyd": self.config["graph"]["ns"],
            },
        )

        graph_dir: pathlib.Path = pathlib.Path(self.config["graph"]["rdf_path"])
        self.domain_path: pathlib.Path = graph_dir / "domain.ttl"
        self.shapes_path: pathlib.Path = graph_dir / "shapes.ttl"
        self.search_path: pathlib.Path = graph_dir / "search.ttl"
        self.pantry_path: pathlib.Path = graph_dir / "pantry.ttl"
        self.corpus_path: pathlib.Path = graph_dir / "corpus.ttl"

        self.load_graph()
        self.kg.load_stottr(graph_dir / "bwyd.stottr")


    def get_cache (
        self,
        *,
        cache_path: pathlib.Path | None = None,
        cache_expire: int | None = None,
        ) -> requests_cache.CachedSession:
        """
Build a URL request cache session, optionally loading any
previous serialized cache from disk.
        """
        if cache_path is None:
            cache_path = pathlib.Path(self.config["bwyd"]["cache_path"])

        if cache_expire is None:
            cache_expire = self.config["bwyd"]["cache_expire"]

        session: requests_cache.CachedSession = requests_cache.CachedSession(
            backend = requests_cache.SQLiteCache(cache_path),
        )

        session.settings.expire_after = cache_expire

        return session


    def load_graph (
        self,
        ) -> None:
        """
Load the graph to verify the RDF semantic descriptions.
        """
        path_list: list[ str ] = [
            self.domain_path,
            self.search_path,
            self.pantry_path,
        ]

        for ttl_path in path_list:
            try:
                self.kg.graph.parse(ttl_path.as_posix())
            except Exception as ex:
                ic(ttl_path)
                traceback.print_exc()


    def iter_recipes (
        self,
        content_path: pathlib.Path,
        *,
        debug: bool = False,
        glob: str = "*.bwyd",
        ) -> typing.Iterator[ tuple[ str, bwyd.Recipe ]]:
        """
Iterate through a directory of Bwyd content.
        """
        ## TEMP MOCK: enumerate via pathlib.glob
        slug_list: list[ str ] = [
            "frozen_gnocchi",
            #"panna_cotta",
            #"gravlax",
        ]

        for slug in slug_list:
            recipe_path: pathlib.Path = content_path / f"{slug}.bwyd"

            recipe: bwyd.Recipe = self.dsl.parse(
                recipe_path,
                slug = slug,
                debug = debug,
            )

            # interpret the parsed module
            recipe.interpret(
                self.account,
                debug = debug,
            )

            yield slug, recipe


    def gen_rdf (
        self,
        content_path: pathlib.Path,
        *,
        debug: bool = False,
        glob: str = "*.bwyd",
        ) -> None:
        """
Iterate through a directory of Bwyd content to parse the recipes,
build the global namespace, generate RDF, then generate HTML.
        """
        bwyd_iter: typing.Iterator[ tuple[ str, bwyd.Recipe ]] = self.iter_recipes(
            content_path,
            debug = debug,
            glob = glob,
        )

        self.bwyd_dict = {}

        for slug, recipe in bwyd_iter:
            self.bwyd_dict[slug] = recipe

            rdf_data: str = "\n".join(
                recipe.gen_rdf(
                    self.account,
                )
            )

            self.kg.gen_ottr_rdf(rdf_data)

        # serialize the full corpus as a graph in TTL format
        with open(self.corpus_path, "w", encoding = "utf-8") as fp:
            ttl: str = self.kg.graph.serialize(format = "turtle")
            fp.write(ttl)

        # SHACL validation
        conforms, results_graph, results_text = self.kg.run_shacl(
            self.corpus_path.as_posix(),
            self.shapes_path.as_posix(),
            self.domain_path.as_posix(),
        )

        if not conforms:
            print(results_text)

        # generate HTML
        html_path: pathlib.Path = recipe.path.with_suffix(".html")

        with open(html_path, "w", encoding = "utf-8") as fp:
            fp.write(recipe.render_template())


    def render_discovery (
        self,
        index_path: pathlib.Path,
        *,
        index_template: jinja2.Template = bwyd.JINJA_INDEX_TEMPLATE,
        ) -> None:
        """
Render an HTML index for search/discovery across a directory of recipes.
        """
        mod_data: dict = {
            "corpus": {
                "icon": bwyd.BWYD_SVG,
                "recipes": [
                    {
                        "slug": recipe.slug,
                        "thumb": recipe.get_thumbnail(self.get_cache()),
                        "title": recipe.title,
                        "text": recipe.text,
                        "serves": recipe.total_yields(),
                        "duration": recipe.total_duration(),
                        "updated": recipe.updated,
                        "keywords": recipe.collect_keywords(),
                    }
                    for recipe in self.bwyd_dict.values()
                ],
            },
        }

        html: str = index_template.render(mod_data)

        with open(index_path, "w", encoding = "utf-8") as fp:
            fp.write(html)



if __name__ == "__main__":
    account: str = "pacoid"
    content_path: pathlib.Path = pathlib.Path("../bwyd-editor/content")

    corpus: Corpus = Corpus(account)
    corpus.gen_rdf(content_path)

    ## build global namespace
    for slug, recipe in corpus.bwyd_dict.items():
        global_ns, local_ns, product_names = recipe.get_product_names(account)
        ic(global_ns, local_ns, product_names)

    ## search/discovery support
    sys.exit(0)

    corpus.render_discovery(
        content_path / "index.html",
    )
