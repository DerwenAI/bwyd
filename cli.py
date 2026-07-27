#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib
import sys

from icecream import ic
import requests_cache

import bwyd


if __name__ == "__main__":
    dsl: bwyd.Bwyd = bwyd.Bwyd(
        config_path = pathlib.Path("config.toml"),
    )

    dsl.extend_converter([
        #bwyd.Conversion.model_validate({ "symbol": "vodka", "density": 222.4, })
    ])


    ## render each module as HTML
    account: str = "pacoid"

    corpus: bwyd.Corpus = dsl.build_corpus()
    dir_path: pathlib.Path = pathlib.Path("examples")

    recipes: list[ bwyd.Recipe ] = list(corpus.parse_recipes(
        account,
        dir_path,
        debug = True, # False
    ))

    for recipe in recipes:
        html_path: pathlib.Path = recipe.path.with_suffix(".html")

        with open(html_path, "w", encoding = "utf-8") as fp:
            fp.write(recipe.render_template())

    ## search/discovery support
    corpus.render_discovery(
        recipes,
        dir_path / "index.html",
    )

    ## KG prototype support
    sys.exit(0)

    graph: bwyd.Graph = corpus.build_graph(recipes)

    with open("kg.rdf", "w", encoding = "utf-8") as fp:
        fp.write(graph.serialize())
