#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import json
import pathlib
import tomllib

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
        *,
        config_path: pathlib.Path | None = None,
        converter: Converter = UNIT_CONVERTER,
        ) -> None:
        """
Constructor.
        """
        self.config: dict = {}

        if config_path is not None:
            with open(config_path, mode = "rb") as fp:
                self.config = tomllib.load(fp)

        self.converter: Converter = converter


    def extend_converter (
        self,
        conversions: list[ Conversion ],
        ) -> None:
        """
Extend the measurements unit converter by merging with provided conversions.
        """
        for conv in conversions:
            self.converter[ conv.symbol ] = conv


    def parse (
        self,
        path: pathlib.Path,
        *,
        slug: str | None = None,
        debug: bool = False,
        ) -> Recipe:
        """
Initialize a parser to load one Bywd module from a file.
        """
        return Recipe(
            path,
            self.META_MODEL.model_from_file(
                path,
                debug = debug,
            ),
            self.converter,
            slug = slug,
        )
