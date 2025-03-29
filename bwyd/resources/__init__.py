#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package definitions for the Bwyd DSL resource files.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import pathlib

import jinja2

_CONVERT_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "convert.json"

_GRAMMAR_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.tx"

_ICON_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.svg"

_JINJA_TEMPLATE: jinja2.Template = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        pathlib.Path(__file__).resolve().parent
    )
).get_template("bwyd.jinja")

_TEMPLATE_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.jinja"



