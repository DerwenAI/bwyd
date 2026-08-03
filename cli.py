#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib

from icecream import ic

import bwyd


if __name__ == "__main__":
    ic.configureOutput(
        noColor = True,
    )

    account: str = "pacoid"
    content_path: pathlib.Path = pathlib.Path("examples")

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    corpus.parse_recipes(content_path)
    corpus.gen_rdf()
    corpus.apply_shacl_rules()
    corpus.build_product_graph()

    corpus.render_discovery(
        content_path / "index.html",
    )
