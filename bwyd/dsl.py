#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import pathlib

from icecream import ic  # type: ignore  # pylint: disable=E0401,W0611
import textx  # type: ignore  # pylint: disable=E0401

from .measure import Converter
from .recipe import Recipe
from .resources import GRAMMAR_PATH


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


    def __init__ (
        self,
        config: dict,
        ) -> None:
        """
Constructor.
        """
        self.config: dict = config


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
