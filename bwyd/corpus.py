#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Represent a corpus of parsed Bwyd modules.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import defaultdict
import logging
import os
import pathlib
import tempfile
import tomllib
import traceback

from icecream import ic
import jinja2
import minify_html
import rdflib
import requests_cache
import xandergraph as xg  # type: ignore

from .dsl import Bwyd
from .measure import Conversion, Converter, Product
from .recipe import Recipe
from .resources import BWYD_SVG, JINJA_INDEX_TEMPLATE, JINJA_PAGE_TEMPLATE


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
        language: str = "en",
        ) -> None:
        """
Constructor.
        """
        with open(config_path, mode = "rb") as fp:
            self.config: dict = tomllib.load(fp)

        logging.basicConfig(
            format = self.config["bwyd"]["log_format"],
        )

        self.language: str = language
        self.account: str = account

        # init the parser and global namespaces
        self.dsl: Bwyd = Bwyd(
            self.config,
        )

        self.bwyd_dict: dict[ str, Recipe ] = {}
        self.errors: list[ str ] = []

        self.product_names: dict[ str, Product ] = {}
        self.product_map: dict[ str, set[ tuple[ str, str ] ] ] = defaultdict(set)

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

        self._load_ontology()
        self.kg.load_stottr(graph_dir / "bwyd.stottr")

        self.keyword_namespace: dict[ str, dict ] = {}
        self.converter: Converter = self._build_pantry_namespace()


    def _load_ontology (
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


    def _build_pantry_namespace (
        self,
        ) -> Converter:
        """
Query the ontology to build a global namespace for ingredients,
e.g., used for measurement conversions, plus a cached namespace
for keywords.
        """
        # query for super+keyword definitions
        query: str = f"""
SELECT DISTINCT ?urn ?definition ?label
WHERE {{
  {{
    ?urn a bwyd:Super .
  }}
  UNION
  {{
    ?urn a bwyd:Keyword .
  }}
  ?urn skos:definition ?definition .
  ?urn skos:prefLabel ?label .
  FILTER(langMatches(lang(?label), "{ self.language }")) .
}}""".strip()

        for row in self.kg.graph.query(query):
            symbol: str = str(row.urn).rsplit(":", maxsplit = 1)[-1]

            self.keyword_namespace[symbol] = {
                "urn": row.urn.n3(),
                "symbol": symbol,
                "label": row.label.toPython(),
                "definition": row.definition.toPython(),
            }

        # query for ingredient densities
        query = """
SELECT DISTINCT ?urn ?density
WHERE {
  ?urn a bwyd:Ingredient .
  ?urn bwyd:density ?density .
}""".strip()

        converter: Converter = {}

        for row in self.kg.graph.query(query):
            conv: Conversion = Conversion(
                symbol = str(row.urn).rsplit(":", maxsplit = 1)[-1],
                density = float(row.density),
            )

            converter[conv.symbol] = conv

        return converter


    def _build_product_namespace (
        self,
        ) -> None:
        """
Iterate through the parsed Bwyd modules to build a global namespace
for products.
        """
        global_ns: str = f"urn:bwyd:{ self.account }"

        # iterate through the corpus to build the product namespace
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
                self.converter,
                slug = slug,
                debug = debug,
            )

            self.bwyd_dict[slug] = recipe

            # interpret the parsed module
            recipe.interpret(
                debug = debug,
            )

        self._build_product_namespace()


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
                recipe.validate_references(
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


    def apply_shacl_rules (
        self,
        ) -> None:
        """
Run the SHACL shape constraint rules to validate the generated RDF.
        """
        self.errors = []

        conforms, error_graph, report = self.kg.run_shacl(
            self.corpus_path.as_posix(),
            self.shapes_path.as_posix(),
            self.domain_path.as_posix(),
        )

        if not conforms:
            print(report)

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


    def build_product_graph (
        self,
        ) -> None:
        """
Query the KG to build a subgraph for closures which produce products.
        """
        # query for product producers
        query: str = """
SELECT DISTINCT ?urn ?product
WHERE {{
  ?urn a bwyd:Closure .
  ?urn bwyd:produces ?product .
}}""".strip()

        for row in self.kg.graph.query(query):
            symbol: str = str(row.product).rsplit(":", maxsplit = 1)[-1]
            path: list[ str ] = str(row.urn).split(":")

            if self.product_names.get(symbol) is None:
                slug: str = path[-2]
                url: str = f"#{ path[-1] }"
            else:
                slug = path[-2]
                url = f"/page/{ path[-2] }"

            self.product_map[slug].add((symbol, url))

        #ic(self.product_map)


    def get_cache_session (
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


######################################################################
## Jinja2 template rendering

    def render_page_meta (
        self,
        recipe: Recipe,
        ) -> dict:
        """
Render metadata in JSON representation which is needed for search/discovery.
        """
        model: dict = {
            "slug": recipe.slug,
            "thumb": recipe.get_thumbnail(self.get_cache_session()),
            "title": recipe.title,
            "text": recipe.text,
            "serves": recipe.total_yields(name_product = False),
            "duration": recipe.total_duration(approximate = True),
            "keywords": recipe.annotate_keywords(keyword_namespace = self.keyword_namespace),
        }

        return model


    def render_page_html (
        self,
        recipe: Recipe,
        *,
        page_template: jinja2.Template = JINJA_PAGE_TEMPLATE,
        minify: bool = True,
        ) -> str:
        """
Load a Jinja2 template and render the data model as HTML,
which is by default minified.
        """
        html: str = page_template.render(
            recipe = recipe.get_model(
                keyword_namespace = self.keyword_namespace,
                product_map = self.product_map,
            )
        )

        if minify:
            return minify_html.minify(  # pylint: disable=E1101
                html,
                keep_html_and_head_opening_tags = True,
                minify_css = True,
                minify_js = True,
                remove_processing_instructions = True,
            )

        return html


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
                fp.write(self.render_page_html(recipe))

        # render the index
        mod_data: dict = {
            "corpus": {
                "icon": BWYD_SVG,
                "recipes": [
                    self.render_page_meta(recipe)
                    for recipe in self.bwyd_dict.values()
                ],
            },
        }

        html: str = index_template.render(mod_data)

        with open(index_path, "w", encoding = "utf-8") as fp:
            fp.write(html)
