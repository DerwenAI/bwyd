#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import json
import logging
import pathlib
import tomllib
import typing

from icecream import ic  # type: ignore  # pylint: disable=E0401
from rdflib.namespace import DCTERMS, RDF, SKOS, XSD  # pylint: disable=W0611
import jinja2
import rdflib
import requests_cache
import textx  # type: ignore  # pylint: disable=E0401

from .measure import Conversion, Converter
from .graph import Graph
from .recipe import Recipe
from .resources import BWYD_SVG, CONVERT_PATH, GRAMMAR_PATH, JINJA_INDEX_TEMPLATE


######################################################################
## corpus operations

class Corpus:  # pylint: disable=R0903
    """
A corpus of Bwyd modules.
    """

    def __init__ (
        self,
        config: dict,
        converter: Converter,
        *,
        lang: str = "en",
        ) -> None:
        """
Constructor.
        """
        logging.basicConfig(format="%(asctime)s %(message)s")

        self.config: dict = config
        self.converter: Converter = converter
        self.lang: str = lang


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


    def iter_files (
        self,
        dir_path: pathlib.Path,
        *,
        glob: str = "*.bwyd",
        ) -> typing.Iterator[ pathlib.Path ]:
        """
Iterator for listing the Bwyd modules in a given directory.
        """
        for bwyd_path in dir_path.rglob(glob):
            # filter out checkpoint files, if any
            # WHERE DO THESE COME FROM?
            if not bwyd_path.stem.endswith("-checkpoint"):
                yield bwyd_path


    def parse_recipes (
        self,
        account: str,
        dir_path: pathlib.Path,
        *,
        glob: str = "*.bwyd",
        debug: bool = False,
        ) -> typing.Iterator[ Recipe ]:
        """
Traverse the given directory, parsing Bwyd modules.
        """
        dsl: Bwyd = Bwyd()

        for bwyd_path in self.iter_files(dir_path, glob = glob):
            slug: str = bwyd_path.stem

            if debug:
                ic(bwyd_path.name)

            # parse the Bwyd module
            recipe: Recipe = dsl.parse(
                bwyd_path,
                slug = slug,
            )

            # interpret the parsed module
            recipe.interpret(
                account,
                debug = debug,
            )

            yield recipe


    def render_discovery (
        self,
        recipes: list[ Recipe ],
        index_path: pathlib.Path,
        *,
        index_template: jinja2.Template = JINJA_INDEX_TEMPLATE,
        ) -> None:
        """
Render an HTML index for search/discovery across a directory of recipes.
        """
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
                    for recipe in recipes
                ],
            },
        }

        html: str = index_template.render(mod_data)

        with open(index_path, "w", encoding = "utf-8") as fp:
            fp.write(html)


    def build_graph (  # pylint: disable=R0914
        self,
        recipes: list[ Recipe ],
        *,
        debug: bool = False,  # pylint: disable=W0613
        ) -> Graph:
        """
Build a knowledge graph from the modules in this corpus.
        """
        graph: Graph = Graph()

        class_closure: rdflib.URIRef = graph.compose_iri_instance("Closure")
        class_ingredient: rdflib.URIRef = graph.compose_iri_instance("Ingredient")
        class_product: rdflib.URIRef = graph.compose_iri_instance("Product")
        class_recipe: rdflib.URIRef = graph.compose_iri_instance("Recipe")
        pred_component_of: rdflib.URIRef = graph.compose_iri_instance("ComponentOf")
        pred_produced_by: rdflib.URIRef = graph.compose_iri_instance("ProducedBy")
        pred_uses_ingredient: rdflib.URIRef = graph.compose_iri_instance("UsesIngredient")

        for recipe in recipes:
            recipe_iri: rdflib.URIRef = graph.compose_iri([ recipe.slug ])  # type: ignore

            graph.add_tuple(
                recipe_iri,
                RDF.type,
                class_recipe,
            )

            for closure_symbol, closure in recipe.closures.items():
                closure_iri: rdflib.URIRef = graph.compose_iri([ recipe.slug, closure_symbol ])  # type: ignore  # pylint: disable=C0301

                graph.add_tuple(
                    closure_iri,
                    RDF.type,
                    class_closure,
                )

                graph.add_tuple(
                    closure_iri,
                    pred_component_of,
                    recipe_iri,
                )

                graph.add_tuple(
                    closure_iri,
                    SKOS.prefLabel,
                    graph.compose_iri_literal(closure.name, lang = self.lang),
                )

                graph.add_tuple(
                    closure_iri,
                    DCTERMS.description,
                    graph.compose_iri_literal(closure.text, lang = self.lang),
                )

                for super_class in closure.supers:
                    super_iri: rdflib.URIRef = graph.compose_iri([ super_class ])

                    graph.add_tuple(
                        closure_iri,
                        RDF.type,
                        super_iri,
                    )

                    graph.add_tuple(
                        closure_iri,
                        SKOS.broader,
                        super_iri,
                    )

                for keyword in closure.keywords:
                    keyword_iri: rdflib.URIRef = graph.compose_iri_instance("Keyword", sub_symbol = keyword)  # pylint: disable=C0301

                    graph.add_tuple(
                        closure_iri,
                        SKOS.related,
                        keyword_iri,
                    )

                for product in closure.products:
                    product_iri: rdflib.URIRef = graph.compose_iri([ recipe.slug, product.symbol ])  # type: ignore  # pylint: disable=C0301

                    graph.add_tuple(
                        product_iri,
                        RDF.type,
                        class_product,
                    )

                    graph.add_tuple(
                        product_iri,
                        pred_produced_by,
                        closure_iri,
                    )

                for dependency in closure.ingredients.values():
                    if not dependency.external:
                        ingredient_iri: rdflib.URIRef = graph.compose_iri_instance("Ingredient", sub_symbol = dependency.symbol)  # pylint: disable=C0301

                        graph.add_tuple(
                            ingredient_iri,
                            RDF.type,
                            class_ingredient,
                        )

                        graph.add_tuple(
                            ingredient_iri,
                            SKOS.prefLabel,
                            graph.compose_iri_literal(dependency.symbol.replace("_", " "), lang = self.lang),  # pylint: disable=C0301
                        )

                        graph.add_tuple(
                            ingredient_iri,
                            DCTERMS.description,
                            graph.compose_iri_literal(dependency.text, lang = self.lang),
                        )
                    else:
                        ingredient_iri = graph.compose_iri([ recipe.slug, dependency.symbol ])  # type: ignore  # pylint: disable=C0301

                    graph.add_tuple(
                        closure_iri,
                        pred_uses_ingredient,
                        ingredient_iri,
                    )

        return graph


######################################################################
## parser/interpreter definitions

class Bwyd:  # pylint: disable=R0903
    """
Bwyd DSL parser/interpreter.
    """
    META_MODEL: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        GRAMMAR_PATH,
        debug = False, # True
    )

    with open(CONVERT_PATH, "r", encoding = "utf-8") as fp:
        UNIT_CONVERTER: Converter = {
            conv.symbol: conv
            for row in json.load(fp)
            for conv in [ Conversion.model_validate(row) ]
        }


    def __init__ (
        self,
        *,
        config_path: pathlib.Path | None = None,
        converter: Converter = UNIT_CONVERTER,
        ) -> None:
        """
Constructor.
        """
        self.config: dict = {}

        if config_path is not None:
            with open(config_path, mode = "rb") as fp:
                self.config = tomllib.load(fp)

        self.converter: Converter = converter


    def extend_converter (
        self,
        conversions: list[ Conversion ],
        ) -> None:
        """
Extend the measurements unit converter by merging with provided conversions.
        """
        for conv in conversions:
            self.converter[ conv.symbol ] = conv


    def parse (
        self,
        path: pathlib.Path,
        *,
        slug: str | None = None,
        debug: bool = False,
        ) -> Recipe:
        """
Initialize a parser to load one Bywd module from a file.
        """
        return Recipe(
            path,
            self.META_MODEL.model_from_file(
                path,
                debug = debug,
            ),
            self.converter,
            slug = slug,
        )


    def build_corpus (
        self,
        ) -> Corpus:
        """
Factory for initializing a corpus of Bywd modules.
        """
        return Corpus(
            config = self.config,
            converter = self.converter,
        )
