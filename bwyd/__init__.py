#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package definitions for the Bwyd DSL.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from .dsl import Bwyd, Corpus, Graph

from .error import BwydParserError

from .kernel import BwydKernel

from .measure import Conversion, Converter, Humanized, \
    MeasureUnits, Measure, \
    DurationUnits, Duration, \
    Temperature

from .module import Module

from .ops import Dependency, DependencyDict, Appliance, \
    OpsTypes, OpNote, OpTransfer, OpAdd, OpAction, OpWait, OpStore, OpHeat, OpChill, OpBake

from .resources import BWYD_NAMESPACE, BWYD_SVG, \
    CONVERT_PATH, GRAMMAR_PATH, ICON_PATH, \
    JINJA_PAGE_TEMPLATE, JINJA_INDEX_TEMPLATE, \
    URL_PATTERN

from .structure import Post, Product, \
    Activity, Focus, Closure
