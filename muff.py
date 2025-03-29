#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parse an example module in the Bwyd language.
"""

import json
import pathlib

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

    #data: dict = module.get_model()

    # render the Jinja2 template
    print(module.render_template())
