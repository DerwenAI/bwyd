#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package definitions for the Bwyd DSL resource files.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import pathlib
import re

import jinja2


BWYD_NAMESPACE: str = "https://derwen.ai/ns/v2/bwyd/"

BWYD_SVG: str = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMTIwMHB0IiBoZWlnaHQ9IjEyMDBwdCIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwIDAgMTIwMCAxMjAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogPHBhdGggdHJhbnNmb3JtPSJtYXRyaXgoMjAuMzM5IDAgMCAyMC4zMzkgMTcyLjg4IDIwLjMzOSkiIGQ9Im01Ljg2NDcgNTYuNjkydi0zMS4yNzhsLTUuODY0Ny00Ljg4NzF2LTIwLjUyNiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iMiIvPgogPHBhdGggdHJhbnNmb3JtPSJtYXRyaXgoLTIwLjMzOSAwIDAgMjAuMzM5IDcyNy42OSAyMC4zMzkpIiBkPSJtMTYuNTcyIDU2LjY5MnYtMzEuMjc4bC01Ljg2NDctNC44ODcxdi0yMC41MjYiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBzdHJva2Utd2lkdGg9IjIiLz4KIDxwYXRoIHRyYW5zZm9ybT0ibWF0cml4KDIwLjMzOSAwIDAgMjAuMzM5IDE3Mi44OCAyMC4zMzkpIiBkPSJtNS4zNTM1IDAuNDg4NjR2MTcuNjIxIiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSIyIi8+CiA8cGF0aCB0cmFuc2Zvcm09Im1hdHJpeCgyMC4zMzkgMCAwIDIwLjMzOSAxNzIuODggMjAuMzM5KSIgZD0ibTExLjIxOCAwLjQ4ODY0djE3LjYyMSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS13aWR0aD0iMiIvPgogPHBhdGggdHJhbnNmb3JtPSJtYXRyaXgoMjAuMzM5IDAgMCAtMjAuMzM5IDE3Mi44OCAxMTc5LjkpIiBkPSJtMjguMTQzIDU0LjIyOHYtMzAuOTYzYy0xMC44NTctMTUuODgyLTkuOTA0OC0yMy42MzIgMi44NTcyLTIzLjI1MSAxMi43NjIgMC4zODA4NSAxMy42NjcgOC4xMzEzIDIuNzE0MiAyMy4yNTF2MzAuOTYzYzAgMS41Mzg0LTEuMjQ3IDIuNzg1Ni0yLjc4NTYgMi43ODU2cy0yLjc4NTgtMS4yNDcyLTIuNzg1OC0yLjc4NTZ6IiBmaWxsPSJub25lIiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMiIvPgogPHBhdGggdHJhbnNmb3JtPSJtYXRyaXgoMjAuMzM5IDAgMCAyMC4zMzkgMTcyLjg4IDIwLjMzOSkiIGQ9Im0yOSAzOGMtMS45OTk5IDIuNjY2Ny0zLjY2NjYgNi4wMDAxLTUgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo="  # pylint: disable=C0301


CONVERT_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "convert.json"

GRAMMAR_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.tx"

ICON_PATH: pathlib.Path = pathlib.Path(__file__).resolve().parent / "bwyd.svg"


_jinja2_env: jinja2.Environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        pathlib.Path(__file__).resolve().parent
    )
)

JINJA_PAGE_TEMPLATE: jinja2.Template = _jinja2_env.get_template("page.jinja")
JINJA_INDEX_TEMPLATE: jinja2.Template = _jinja2_env.get_template("index.jinja")


URL_PATTERN: re.Pattern = re.compile(
    r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))"""  # pylint: disable=C0301
)
