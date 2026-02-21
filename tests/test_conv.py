#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unit tests:

  * converter

see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import json
import pathlib
import sys

import bwyd  # pylint: disable=C0413,E0401


def test_converter (
    *,
    debug: bool = False,
    ) -> None:
    """
Test example conversions.
    """
    dsl: bwyd.Bwyd = bwyd.Bwyd()

    ## 25 g sugar == 2 tbsp

    symbol: str = "sugar"

    measure: bwyd.Measure = bwyd.Measure(
        amount = 25.0,
        units = "g",
    )

    obs_conv: str = measure.humanize_convert(
        symbol,
        True,
        dsl.converter,
    )

    if debug:
        print(obs_conv)

    exp_conv: str = "25 g (2 tbsps)"

    # compare
    assert obs_conv == exp_conv


if __name__ == "__main__":
    test_converter(debug = True)
