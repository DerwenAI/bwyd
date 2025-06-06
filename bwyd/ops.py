#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Operations objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
import enum
import typing

from pydantic import BaseModel, NonNegativeInt

from .measure import Converter, Measure, DurationUnits, Duration, Temperature


######################################################################
## dependencies

class Dependency (BaseModel):  # pylint: disable=R0902
    """
A data class representing one parsed dependency:
Ingredient, Tool, Container, etc.
    """
    loc: dict
    symbol: str
    text: str
    ref_count: NonNegativeInt = 0
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

class Appliance (enum.StrEnum):
    """
An enumeration class representing string literals for kinds of appliances.
    """
    GENERIC = enum.auto()
    STOVE = enum.auto()
    COOLER = enum.auto()
    OVEN = enum.auto()


class OpGeneric (BaseModel):  # pylint: disable=R0902
    """
A data class representing a generic operation.
    """
    loc: dict
    ref_count: NonNegativeInt = 0


    def get_duration (
        self,
        ) -> Duration:
        """
Stub: Total duration.
        """
        return Duration(
            amount = 0.0,
            units = DurationUnits.SECOND.value,
        )


class OpNote (OpGeneric):  # pylint: disable=R0902
    """
Represents a collapsable Note, inline *within* an Activity, from the
Author/Cook for other Cooks.
    """
    text: str


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "note": {
                "text": self.text,
            }
        }


class OpTransfer (OpGeneric):  # pylint: disable=R0902
    """
Represents the action of a Cook to Transfer an intermediate into
a Container from another Focus, still *within* the same Closure.
    """
    symbol: str
    entity: Dependency


    def get_model (
        self,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "transfer": {
                "name": self.symbol,
            },
        }


class OpAdd (OpGeneric):  # pylint: disable=R0902
    """
Represents the action of a Cook to Add a measured amount of an
ingredient into a Container within an Activity.
    """
    symbol: str
    measure: Measure
    text: str
    entity: Dependency


    def get_model (
        self,
        converter: Converter,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        amount: str = self.measure.humanize_convert(
            self.symbol,
            self.entity.external,
            converter,
        )

        return {
            "name": self.symbol,
            "amount": amount,
            "text": self.text,
        }


class OpAction (OpGeneric):  # pylint: disable=R0902
    """
Represents the action of a Cook using a Tool to perform part of an
Activity on the food within a specific Container.
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


class OpStore (OpGeneric):  # pylint: disable=R0902
    """
Represents the process of a Cook on a Container to store the yield of
a Closure for a specified time period.
    """
    container: Dependency
    modifier: str
    duration: Duration


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "store": {
                "text": self.modifier,
                "upto": self.duration.humanize(),
            }
        }


class OpAppliance (OpGeneric):  # pylint: disable=R0902
    """
Represents the process of an Appliance operating on the food within
a specific Container as part of an Activity.
    """
    container: Dependency
    modifier: str
    until: str
    duration: Duration
    appliance: str = Appliance.GENERIC


    def get_duration (
        self,
        ) -> Duration:
        """
Duration of this operation.
        """
        return self.duration


class OpHeat (OpAppliance):  # pylint: disable=R0902
    """
Represents an Appliance: stove, range, hotplate, camp fire --
used to *heat* in different modes.
    """
    appliance: str = Appliance.STOVE


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            self.appliance: {
                "text": self.modifier,
                "until": self.until,
                "time": self.duration.humanize(),
            }
        }


class OpChill (OpHeat):  # pylint: disable=R0902
    """
Represents an Appliance: cooler --
used to *chill* in different modes.
    """
    appliance: str = Appliance.COOLER


class OpBake (OpAppliance):  # pylint: disable=R0902
    """
Represents an Appliance: oven --
used to *bake* in different modes.
    """
    mode: str
    temperature: Temperature
    appliance: str = Appliance.OVEN


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            self.appliance: {
                "text": self.modifier,
                "until": self.until,
                "time": self.duration.humanize(),
                "mode": self.mode.lower(),
                "temperature": self.temperature.humanize(),
            }
        }


OpsTypes = typing.Union[
    OpNote,
    OpTransfer,
    OpAdd,
    OpAction,
    OpStore,
    OpHeat,
    OpChill,
    OpBake,
]
