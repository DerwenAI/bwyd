#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script.
"""

import pathlib
import sys
import traceback
import typing

from icecream import ic
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

        self.dsl: bwyd.Bwyd = bwyd.Bwyd(
            config_path = config_path,
        )

        # init the graph and load the OTTR templates
        self.kg: xg.KnowledgeGraph = xg.KnowledgeGraph(
            ns = {
                "bwyd": self.dsl.config["graph"]["ns"],
            },
        )

        graph_dir: pathlib.Path = pathlib.Path(self.dsl.config["graph"]["rdf_path"])
        self.domain_path: pathlib.Path = graph_dir / "domain.ttl"
        self.shapes_path: pathlib.Path = graph_dir / "shapes.ttl"
        self.search_path: pathlib.Path = graph_dir / "search.ttl"
        self.pantry_path: pathlib.Path = graph_dir / "pantry.ttl"
        self.corpus_path: pathlib.Path = graph_dir / "corpus.ttl"

        self.load_graph()
        self.kg.load_stottr(graph_dir / "bwyd.stottr")


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
            "panna_cotta",
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
Iterate through a directory of Bwyd content to parse recipes and
generate RDF.
        """
        iter_bwyd: typing.Iterator[ tuple[ str, bwyd.Recipe ]] = self.iter_recipes(
            content_path,
            debug = debug,
            glob = glob,
        )

        for slug, recipe in iter_bwyd:
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


if __name__ == "__main__":
    account: str = "pacoid"
    corpus: Corpus = Corpus(account)

    content_path: pathlib.Path = pathlib.Path("../bwyd-editor/content")
    corpus.gen_rdf(content_path)
