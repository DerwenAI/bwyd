#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Represent a corpus of parsed Bwyd modules.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import logging
import os
import pathlib
import tempfile
import traceback

from icecream import ic
import jinja2
import rdflib
import requests_cache
import xandergraph as xg  # type: ignore

from .dsl import Bwyd
from .measure import Converter, Product
from .recipe import Recipe
from .resources import BWYD_SVG, JINJA_INDEX_TEMPLATE


######################################################################
## corpus definitions

class Corpus:  # pylint: disable=R0902
    """
Manage a corpus of Bwyd modules.
    """

    def __init__ (
        self,
        account: str,
        *,
        config_path: pathlib.Path = pathlib.Path("config.toml"),
        converter: Converter = Bwyd.UNIT_CONVERTER,  # pylint: disable=W0613
        lang: str = "en",
        ) -> None:
        """
Constructor.
        """
        self.lang: str = lang
        self.account: str = account
        self.bwyd_dict: dict[ str, Recipe ] = {}
        self.product_names: dict[ str, Product ] = {}
        self.errors: list[ str ] = []

        self.dsl: Bwyd = Bwyd(
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

        self.load_ontology()
        self.kg.load_stottr(graph_dir / "bwyd.stottr")


    def load_ontology (
        self,
        ) -> None:
        """
Load the RDF semantic descriptions (TBox) into the knowledge graph,
with exception handling to identify any errors.
        """
        path_list: list[ pathlib.Path ] = [
            self.domain_path,
            self.search_path,
            self.pantry_path,
        ]

        for ttl_path in path_list:
            try:
                self.kg.graph.parse(ttl_path.as_posix())
            except Exception as ex:  # pylint: disable=W0612,W0718
                ic(ttl_path)
                traceback.print_exc()


    def parse_recipes (
        self,
        content_path: pathlib.Path,
        *,
        glob: str = "*.bwyd",
        debug: bool = False,
        ) -> None:
        """
Iterate through a directory of Bwyd content to parse the recipes.
        """
        self.bwyd_dict = {}

        for recipe_path in content_path.glob(glob):
            slug: str = recipe_path.stem

            recipe: Recipe = self.dsl.parse(
                recipe_path,
                slug = slug,
                debug = debug,
            )

            self.bwyd_dict[slug] = recipe

            # interpret the parsed module
            recipe.interpret(
                debug = debug,
            )


    def build_namespace (
        self,
        ) -> None:
        """
Iterate through the parsed Bwyd modules to build a global namespace
for products.
        """
        global_ns: str = f"urn:bwyd:{ self.account }"

        for recipe in self.bwyd_dict.values():
            for closure in recipe.closures.values():
                for product in closure.products:
                    if not product.intermediate and product.urn is None:
                        product.urn = f"{ global_ns }:product:{ product.symbol }"

                        if product.symbol in self.product_names:
                            print(
                                f"CONFLICT: product { product.symbol } overlaps:",
                                self.product_names[product.symbol].urn,
                                product.urn,
                            )
                        else:
                            self.product_names[product.symbol] = product


    def gen_rdf (
        self,
        ) -> None:
        """
Iterate through the parsed Bwyd modules to generate RDF.
        """
        tf: tempfile._TemporaryFileWrapper = tempfile.NamedTemporaryFile(  # pylint: disable=R1732
            suffix = ".ttl",
            delete = False,
        )

        with open(tf.name, "w", encoding = "utf-8") as fp:
            for recipe in self.bwyd_dict.values():
                recipe.validate(
                    self.account,
                    self.product_names,
                )

                rdf_data: list[ str ] = recipe.gen_rdf(
                    self.account,
                    self.product_names,
                )

                tmp_graph: rdflib.Graph = rdflib.Graph()

                tmp_graph.bind(
                    "bwyd",
                    rdflib.Namespace(self.config["graph"]["ns"]),
                )

                self.kg.gen_ottr_rdf(
                    "\n".join(rdf_data),
                    tmp_graph,
                )

                fp.write(tmp_graph.serialize(format = "turtle"))

        tf.close()
        self.kg.graph.parse(tf.name)

        tf.close()
        os.unlink(tf.name)

        # serialize the full corpus as a graph in TTL format
        with open(self.corpus_path, "w", encoding = "utf-8") as fp:
            ttl: str = self.kg.graph.serialize(format = "turtle")
            fp.write(ttl)


    def shacl_rules (
        self,
        ) -> None:
        """
Run the SHACL shape constraint rules to validate the generated RDF.
        """
        self.errors = []

        conforms, error_graph, _ = self.kg.run_shacl(
            self.corpus_path.as_posix(),
            self.shapes_path.as_posix(),
            self.domain_path.as_posix(),
        )

        if not conforms:
            query: str = """
SELECT DISTINCT ?focus ?message
WHERE {
  ?anode sh:result ?bnode .
  ?bnode sh:focusNode ?focus . 
  ?bnode sh:resultMessage ?message .
}"""
            self.errors = sorted([
                row.message
                for row in error_graph.query(query)
            ])


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


    def render_discovery (
        self,
        index_path: pathlib.Path,
        *,
        index_template: jinja2.Template = JINJA_INDEX_TEMPLATE,
        ) -> None:
        """
Generate HTML pages plus an index for search/discovery across a
corpus of recipes.
        """
        for recipe in self.bwyd_dict.values():
            html_path: pathlib.Path = recipe.path.with_suffix(".html")

            with open(html_path, "w", encoding = "utf-8") as fp:
                fp.write(recipe.render_template())

        # render the index
        mod_data: dict = {
            "corpus": {
                "icon": BWYD_SVG,
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
