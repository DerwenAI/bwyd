#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package definitions for the Bwyd DSL.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from .kernel import BwydKernel

from .parser import Bwyd

from .objects import Duration, Measure, \
    OpAction, OpAdd, OpChill, OpUse, OpsTypes, \
    Closure, Focus


__version__ = "0.1"

__release__ = __version__

__title__ = "Bwyd DSL"

__description__ = "Bwyd DSL for kitchen engineering"

__copyright__ = "2024, Derwen, Inc."

__author__ = """\n""".join([
    "derwen.ai <info@derwen.ai>"
])
