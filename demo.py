#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An example module in the Bwyd language.
"""

import json
import pathlib

from icecream import ic
import bwyd


if __name__ == "__main__":
    # parse an example Bwyd module
    module: bwyd.Module = bwyd.Bwyd.parse(
        pathlib.Path("examples/gnocchi.bwyd"),
        debug = False, # True
    )

    # interpret the parsed module
    module.interpret(
        debug = True, # False
    )

    # make a summary report
    print(json.dumps(
        module.to_json(),
        indent = 2,
        sort_keys = False,
    ))
