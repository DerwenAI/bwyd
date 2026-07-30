#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import json
import pathlib

from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611
import textx  # type: ignore  # pylint: disable=E0401

from .measure import Conversion, Converter
from .recipe import Recipe
from .resources import CONVERT_PATH, GRAMMAR_PATH


######################################################################
## parser/interpreter definitions

class Bwyd:  # pylint: disable=R0903
    """
Bwyd DSL parser/interpreter.
    """
    META_MODEL: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        GRAMMAR_PATH,
        debug = False, # True
    )

    with open(CONVERT_PATH, "r", encoding = "utf-8") as fp:
        UNIT_CONVERTER: Converter = {
            conv.symbol: conv
            for row in json.load(fp)
            for conv in [ Conversion.model_validate(row) ]
        }


    def __init__ (
        self,
        config: dict,
        converter: Converter,
        ) -> None:
        """
Constructor.
        """
        self.config: dict = config
        self.converter: Converter = converter


    def parse (
        self,
        path: pathlib.Path,
        converter: Converter,
        *,
        slug: str | None = None,
        debug: bool = False,
        ) -> Recipe:
        """
Parse one Bywd module from a file.
        """
        return Recipe(
            path,
            self.META_MODEL.model_from_file(
                path,
                debug = debug,
            ),
            converter,
            slug = slug,
        )
