#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parse an example module in the Bwyd language.
"""

from collections import OrderedDict
import json
import pathlib
import sys

from icecream import ic
import bwyd


if __name__ == "__main__":
    slug: str = "applesauce_muffins"
    muff_path: pathlib.Path = pathlib.Path("examples") / f"{slug}.bwyd"

    # parse an example Bwyd module
    module: bwyd.Module = bwyd.Bwyd.parse(
        muff_path,
        slug = slug,
        debug = False, # True
    )


    # interpret the parsed module
    module.interpret(
        debug = True, # False
    )

    #data: dict = module.get_model()

    # render the Jinja2 template
    html: str = module.render_template()
    print(html)
