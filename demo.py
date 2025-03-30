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

    # output a JSON model, for use in unit tests
    print(json.dumps(
        module.get_model(),
        indent = 2,
        sort_keys = False,
    ))

    # render the Jinja2 HTML template
    with open("gnoc.html", "w", encoding = "utf-8") as fp:
        fp.write(module.render_template())
