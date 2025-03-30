#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Operations objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
from dataclasses import dataclass
import typing

from .measure import Measure, Duration, Temperature


######################################################################
## dependencies

@dataclass(order = False, frozen = False, kw_only = True)
class Dependency:  # pylint: disable=R0902
    """
A data class representing one parsed dependency:
Ingredient, Tool, Container, etc.
    """
    loc: dict
    symbol: str
    text: str
    ref_count: int = 0
    external: bool = False

    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "name": self.symbol,
            "text": self.text,
        }


class DependencyDict (OrderedDict):
    """
A dictionary of a specific class of dependencies, which also provides
a local namespace.
    """

    def get_model (
        self
        ) -> list:
        """
Serializable representation for JSON.
        """
        return [ dep.get_model() for dep in self.values() ]


######################################################################
## operations

@dataclass(order = False, frozen = False, kw_only = True)
class OpGeneric:  # pylint: disable=R0902
    """
A data class representing a generic operation.
    """
    loc: dict
    ref_count: int = 0


    def get_duration (
        self,
        ) -> Duration:
        """
Stub: Total duration.
        """
        return Duration(0, "sec")


@dataclass(order = False, frozen = False)
class OpAdd (OpGeneric):  # pylint: disable=R0902
    """
A data class representing one Add object.
    """
    symbol: str
    measure: Measure
    text: str


    def get_model (
        self,
        converter: dict,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        amount: str = self.measure.humanize()

        # show conversion, if available
        if self.symbol in converter:
            _, metric_units, ratio = converter[self.symbol]

            if self.measure.units == metric_units:
                imper_amount: float = self.measure.amount / ratio
                amount += f" ({self.measure.humanize_cup(imper_amount)})"

        return {
            "name": self.symbol,
            "amount": amount,
            "text": self.text,
        }


@dataclass(order = False, frozen = False)
class OpAction (OpGeneric):  # pylint: disable=R0902
    """
A data class representing one Action object.
    """
    tool: Dependency
    modifier: str
    until: str
    duration: Duration


    def get_duration (
        self,
        ) -> Duration:
        """
Duration of this operation.
        """
        return self.duration


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "action": {
                "tool": self.tool.symbol,
                "verb": self.modifier,
                "text": self.until,
                "time": self.duration.humanize(),
            }
        }


@dataclass(order = False, frozen = False)
class OpBake (OpGeneric):  # pylint: disable=R0902
    """
A data class representing one Bake object.
    """
    mode: str
    container: Dependency
    modifier: str
    until: str
    duration: Duration
    temperature: Temperature


    def get_duration (
        self,
        ) -> Duration:
        """
Duration of this operation.
        """
        return self.duration


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "bake": {
                "mode": self.mode.lower(),
                "temperature": self.temperature.humanize(),
                "text": self.modifier,
                "until": self.until,
                "time": self.duration.humanize(),
            }
        }


@dataclass(order = False, frozen = False)
class OpChill (OpGeneric):  # pylint: disable=R0902
    """
A data class representing one Chill object.
    """
    container: Dependency
    modifier: str
    until: str
    duration: Duration

    def get_duration (
        self,
        ) -> Duration:
        """
Duration of this operation.
        """
        return self.duration


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "chill": {
                "text": self.modifier,
                "until": self.until,
                "time": self.duration.humanize(),
            }
        }


OpsTypes = typing.Union[ OpAdd, OpAction, OpBake, OpChill ]
