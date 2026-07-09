#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An example module in the Bwyd language.
"""

import json
import pathlib
import sys

from deepdiff import DeepDiff
from icecream import ic
import bwyd


if __name__ == "__main__":
    examples_path: pathlib.Path = pathlib.Path("test")
    slug: str = "min_eval"

    ## OVERRIDES
    examples_path = pathlib.Path(".")
    slug = sys.argv[1]


    ######################################################################
    # parse an example Bwyd module
    dsl: bwyd.Bwyd = bwyd.Bwyd(
        config_path = pathlib.Path("config.toml"),
    )

    module: bwyd.Recipe = dsl.parse(
        examples_path / f"{slug}.bwyd",
        slug = slug,
        debug = False, # True
    )

    # interpret the parsed module
    module.interpret(
        debug = True, # False
    )

    observed: dict = module.get_model()

    # output a JSON model, for use in unit tests
    with open(examples_path / f"{slug}.json", "w", encoding = "utf-8") as fp:
        fp.write(json.dumps(
            observed,
            indent = 2,
            sort_keys = False,
        ))


    ######################################################################
    # only go this far
    sys.exit(0)

    # compare with expected results
    with open("expect.json", "r", encoding = "utf-8") as fp:
        expected: dict = json.load(fp)

    ic(DeepDiff(expected, observed))

    # render the Jinja2 HTML template
    with open(examples_path / f"{slug}.html", "w", encoding = "utf-8") as fp:
        fp.write(module.render_template())
