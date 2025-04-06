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
    examples_path: pathlib.Path = pathlib.Path("examples")
    slug: str = "applesauce_muffins"

    # parse an example Bwyd module
    module: bwyd.Module = bwyd.Bwyd.parse(
        examples_path / f"{slug}.bwyd",
        slug = slug,
        debug = False, # True
    )


    # interpret the parsed module
    module.interpret(
        debug = True, # False
    )

    #data: dict = module.get_model()

    # render the Jinja2 HTML template
    with open(examples_path / f"{slug}.html", "w", encoding = "utf-8") as fp:
        fp.write(module.render_template())
