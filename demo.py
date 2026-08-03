#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script.
"""

import pathlib
import sys

from icecream import ic
import bwyd


if __name__ == "__main__":
    ic.configureOutput(
        noColor = True,
    )

    account: str = "pacoid"
    content_path: pathlib.Path = pathlib.Path("../bwyd-editor/content")

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    corpus.parse_recipes(content_path)
    corpus.gen_rdf()
    corpus.apply_shacl_rules()
    corpus.build_product_graph()

    ic(corpus.product_names.keys())
    ic(corpus.errors)
