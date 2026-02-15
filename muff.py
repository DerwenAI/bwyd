#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib
import sys
import typing

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
    corpus: bwyd.Corpus = dsl.build_corpus()
    dir_path: pathlib.Path = pathlib.Path("examples")

    module_iter: typing.Iterator[ bwyd.Module ] = corpus.parse_modules(
        dir_path,
        #glob = "potato*.bwyd",
        debug = True, # False
    )

    modules: list[ bwyd.Module ] = []

    for module in module_iter:
        modules.append(module)

        # render HTML using the Jinja2 template
        html_path: pathlib.Path = module.path.with_suffix(".html")

        with open(html_path, "w", encoding = "utf-8") as fp:
            fp.write(module.render_template())

    ## search/discovery support
    corpus.render_discovery(
        modules,
        dir_path / "index.html",
    )


    ## KG prototype support
    sys.exit(0)

    graph: bwyd.Graph = corpus.build_graph(modules)

    with open("kg.rdf", "w", encoding = "utf-8") as fp:
        fp.write(graph.serialize())
