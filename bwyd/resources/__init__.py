#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package definitions for the Bwyd DSL resource files.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import pathlib

_CONVERT_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "convert.json"
_GRAMMAR_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.tx"
_ICON_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.svg"
_TEMPLATE_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.jinja"
