#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import pathlib
import typing

import textx  # type: ignore  # pylint: disable=E0401

from .module import Module
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


    @classmethod
    def parse (
        cls,
        script: pathlib.Path,
        *,
        slug: typing.Optional[ str ] = None,
        debug: bool = False,
        ) -> Module:
        """
Parse one Bywd module (a file).
        """
        return Module(
            cls.META_MODEL.model_from_file(
                script,
                debug = debug,
            ),
            slug = slug,
        )
