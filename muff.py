#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parse an example module in the Bwyd language.
"""

import json
import pathlib

from icecream import ic
import bwyd
import jinja2


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

    # load Jinja2 template
    env = jinja2.Environment(loader = jinja2.FileSystemLoader("bwyd/resources"))
    template = env.get_template("bwyd.jinja")

    # format a data model as HTML
    data: dict = module.get_model()
    output = template.render(module = data)
    print(output)
