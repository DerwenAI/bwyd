#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit tests:

  * parser

see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import json
import pathlib
import sys

TEST_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "examples"
sys.path.insert(0, str(TEST_DIR))
import bwyd  # pylint: disable=C0413,E0401


def test_parser (
    *,
    debug: bool = False,
    ) -> None:
    """
Load a sample file to ensure the parser works correctly.
    """
    module: bwyd.Module = bwyd.Bwyd.parse(
        TEST_DIR / "gnocchi.bwyd",
        debug = False, # True
    )

    module.interpret(
        debug = False, # True
    )

    obs_data: list = module.get_model()

    if debug:
        print(json.dumps(obs_data, indent = 2, sort_keys = False,))

    exp_data: dict = json.load(open(TEST_DIR / "gnocchi.json", "r", encoding = "utf-8"))  # pylint: disable=R1732

    # compare
    assert sorted(obs_data.items()) == sorted(exp_data.items())


if __name__ == "__main__":
    test_parser(debug = True)
