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
    examples_path: pathlib.Path = pathlib.Path("examples")
    slug: str = "panna_cotta"

    # parse an example Bwyd module
    dsl: bwyd.Bwyd = bwyd.Bwyd(
        config_path = pathlib.Path("config.toml"),
    )

    module: bwyd.Module = dsl.parse(
        examples_path / f"{slug}.bwyd",
        slug = slug,
        debug = False, # True
    )

    # interpret the parsed module
    module.interpret(
        debug = True, # False
    )

    # output a JSON model, for use in unit tests
    with open(examples_path / f"{slug}.json", "w", encoding = "utf-8") as fp:
        fp.write(json.dumps(
            module.get_model(),
            indent = 2,
            sort_keys = False,
        ))

    # render the Jinja2 HTML template
    with open(examples_path / f"{slug}.html", "w", encoding = "utf-8") as fp:
        fp.write(module.render_template())
