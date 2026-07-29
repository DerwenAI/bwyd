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
    account: str = "pacoid"
    content_path: pathlib.Path = pathlib.Path("examples")

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    corpus.dsl.extend_converter([
        #bwyd.Conversion.model_validate({ "symbol": "vodka", "density": 222.4, })
    ])

    corpus.parse_recipes(content_path)
    corpus.build_namespace()
    corpus.gen_rdf()

    corpus.render_discovery(
        content_path / "index.html",
    )
