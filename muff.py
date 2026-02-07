#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib
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
    examples_path: pathlib.Path = pathlib.Path("examples")

    modules: typing.List[ bwyd.Module ] = corpus.render_html_files(
        examples_path,
        #glob = "potato*.bwyd",
        #glob = "app*.bwyd",
        debug = True, # False
    )


    ## search/discovery support
    corpus.render_discovery(
        modules,
        examples_path / "index.html",
    )


    ## KG prototype support
    graph: bwyd.Graph = corpus.build_graph(modules)

    with open("kg.rdf", "w", encoding = "utf-8") as fp:
        fp.write(graph.serialize())
