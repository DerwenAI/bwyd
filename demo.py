#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example program in the Bwyd language.
"""

import json
import pathlib

from icecream import ic
import bwyd


if __name__ == "__main__":
    ## parse an example Bwyd program
    bwyd_int: bwyd.Bwyd = bwyd.Bwyd()
    ic(bwyd_int)

    prog = bwyd_int.parse(
        pathlib.Path("gnocchi.bwyd"),
        debug = False, # True
    )

    ## interpret the parsed program
    bwyd_int.interpret(
        prog,
        debug = True, # False
    )

    ## make a summary report
    print(json.dumps(
        bwyd_int.to_json(),
        indent = 2,
        sort_keys = False,
    ))
