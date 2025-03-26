#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parse an example module in the Bwyd language.
"""

import json
import pathlib
import sys

from icecream import ic
import bwyd


if __name__ == "__main__":
    # parse an example Bwyd module
    module: bwyd.Module = bwyd.Bwyd.parse(
        pathlib.Path("examples/applesauce_muffins.bwyd"),
        debug = False, # True
    )

    # interpret the parsed module
    module.interpret(
        debug = True, # False
    )

    print(json.dumps(
        module.get_model(),
        indent = 2,
        sort_keys = False,
    ))

    sys.exit(0)

    # format as HTML
    print(module.to_html(indent = True))
