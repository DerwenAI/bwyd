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
    bwyd_int: bwyd.Bwyd = bwyd.Bwyd()
    ic(bwyd_int)

    module = bwyd_int.parse(
        pathlib.Path("examples/gnocchi.bwyd"),
        debug = False, # True
    )

    # interpret the parsed module
    bwyd_int.interpret(
        module,
        debug = True, # False
    )

    # make a summary report
    print(json.dumps(
        bwyd_int.to_json(),
        indent = 2,
        sort_keys = False,
    ))
