#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib

import bwyd


if __name__ == "__main__":
    account: str = "pacoid"
    content_path: pathlib.Path = pathlib.Path("examples")

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    corpus.parse_recipes(content_path)
    corpus.build_namespace()
    corpus.gen_rdf()
    corpus.shacl_rules()

    corpus.render_discovery(
        content_path / "index.html",
    )
