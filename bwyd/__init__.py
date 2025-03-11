#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package definitions for the Bwyd DSL.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from .kernel import BwydKernel

from .parser import Bwyd

from .objects import Dependency, DependencyDict, \
    Measure, Duration, Temperature, \
    OpAdd, OpUse, OpAction, OpBake, OpChill, \
    Focus, Closure


__version__ = "0.2"

__release__ = __version__

__title__ = "Bwyd DSL"

__description__ = "Bwyd DSL for cooking"

__copyright__ = "2024-2025, Derwen, Inc."

__author__ = """\n""".join([
    "derwen.ai <info@derwen.ai>"
])
