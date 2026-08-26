#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit tests:

  * validate the generated RDF with SHACL rules

see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import json
import pathlib
import sys
import warnings

CONTENT_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "examples"
sys.path.insert(0, str(CONTENT_PATH))

import bwyd  # pylint: disable=C0413,E0401


def test_shacl (
    *,
    debug: bool = False,
    ) -> None:
    """
Validate the generated RDF with SHACL rules.
    """
    account: str = "pacoid"

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    with warnings.catch_warnings(action = "ignore"):
        corpus.parse_recipes(CONTENT_PATH)
        corpus.gen_rdf()
        corpus.apply_shacl_rules()

    if len(corpus.errors) > 0:
        for error in corpus.errors:
            print(error)
    
    assert len(corpus.errors) == 0


if __name__ == "__main__":
    test_shacl(debug = True)
