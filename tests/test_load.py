#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit tests:

  * parser loads a Bwyd module

see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import json
import pathlib
import sys

CONTENT_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "examples"
sys.path.insert(0, str(CONTENT_DIR))

import bwyd  # pylint: disable=C0413,E0401


def test_parser (
    *,
    debug: bool = False,
    ) -> None:
    """
Load a sample file to ensure the parser works correctly.
    """
    account: str = "pacoid"

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    slug: str = "frozen_gnocchi"
    bwyd_path: pathlib.Path = CONTENT_DIR / f"{slug}.bwyd"

    recipe: bwyd.Recipe = corpus.dsl.parse(
        bwyd_path,
        corpus.converter,
        slug = slug,
        debug = False, # True
    )

    recipe.interpret(
        debug = False, # True
    )

    obs_data: list = recipe.get_model(account)

    if debug:
        print(json.dumps(obs_data, indent = 2, sort_keys = False,))

    json_path: pathlib.Path = CONTENT_DIR / f"{slug}.json"
    exp_data: dict = json.load(open(json_path, "r", encoding = "utf-8"))  # pylint: disable=R1732
    identical: bool = sorted(obs_data.items()) == sorted(exp_data.items())

    if not identical:
        with open(json_path.with_suffix(".fail"), "w", encoding = "utf-8") as fp:
            fp.write(json.dumps(obs_data, indent = 2, sort_keys = False,))

    # compare
    assert identical


if __name__ == "__main__":
    test_parser(debug = True)
