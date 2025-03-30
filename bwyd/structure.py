#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from dataclasses import dataclass, field
import itertools
import typing

from .measure import Measure

from .ops import Dependency, DependencyDict, \
    OpsTypes, OpAdd


######################################################################
## structural classes

@dataclass(order = False, frozen = False)
class Activity:  # pylint: disable=R0902
    """
A data class representing one Header object.
    """
    text: str
    ops: typing.List[ OpsTypes ] = field(default_factory = lambda: [])


    def get_model (
        self,
        converter: dict,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "title": self.text,
            "steps": [
                {
                    "ingredients": [
                        op.get_model(converter)
                        for op in self.ops
                        if isinstance(op, OpAdd)
                    ]
                }
            ]
        }

        for op in self.ops:
            if not isinstance(op, OpAdd):
                dat["steps"].append(op.get_model())

        return dat


@dataclass(order = False, frozen = False)
class Focus:  # pylint: disable=R0902
    """
A data class representing a parsed Focus object.
    """
    container: Dependency
    activities: typing.List[ Activity ] = field(default_factory = lambda: [])


    def get_model (
        self,
        converter: dict,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "container": self.container.symbol,
            "activities": [ act.get_model(converter) for act in self.activities ],
        }


@dataclass(order = False, frozen = False)
class Closure:  # pylint: disable=R0902
    """
A data class representing one parsed Closure object.
    """
    name: str
    obj: typing.Any
    yields: Measure
    export: typing.Optional[ str ] = None
    text: str = ""
    containers: DependencyDict = field(default_factory = lambda: DependencyDict())  # pylint: disable=W0108
    tools: DependencyDict = field(default_factory = lambda: DependencyDict())  # pylint: disable=W0108
    ingredients: DependencyDict = field(default_factory = lambda: DependencyDict())  # pylint: disable=W0108
    foci: typing.List[ Focus ] = field(default_factory = lambda: [])


    def get_dependencies (
        self
        ) -> list:
        """
Serialized representation in JSON for the containers and tools.
        """
        return [
            dep.get_model()
            for dep in itertools.chain(self.containers.values(), self.tools.values())
        ]
