#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script.
"""

import pathlib
import sys

import bwyd


if __name__ == "__main__":
    account: str = "pacoid"
    content_path: pathlib.Path = pathlib.Path("../bwyd-editor/content")

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    corpus.parse_recipes(content_path)
    corpus.build_namespace()
    corpus.gen_rdf(gen_html = False)
