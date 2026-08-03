#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Operations objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
import enum
import typing

from icecream import ic  # pylint: disable=W0611
from pydantic import BaseModel, NonNegativeInt

from .measure import Converter, \
    Duration, DurationUnits, Measure, Temperature, \
    Product


######################################################################
## notes

class Note (BaseModel):
    """
Represents a collapsable Note, inline *within* Activity, etc.
    """
    loc: dict
    text: str


    def get_model (
        self,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "note": {
                "text": self.text,
            }
        }

        return dat


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
    note: Note | None = None


    def get_model (
        self,
        *,
        pluralize: bool = True,  # pylint: disable=W0613
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "name": self.symbol,
            "text": self.text,
        }

        if self.note is not None:
            dat.update(self.note.get_model())

        return dat


class DependencyDict (OrderedDict):
    """
A dictionary of a specific class of dependencies, which also provides
a local namespace.
    """
    def get_model (
        self,
        *,
        pluralize: bool = True,  # pylint: disable=W0613
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
    note: Note | None = None
    ref_count: NonNegativeInt = 0


    def get_duration (
        self,
        *,
        pluralize: bool = True,  # pylint: disable=W0613
        ) -> Duration:
        """
Stub: Total duration.
        """
        return Duration(
            amount = 0.0,
            units = DurationUnits.SECOND.value,
        )


class OpAdd (OpGeneric):  # pylint: disable=R0902
    """
Represents the action of a Cook to Add a measured amount of an
ingredient into a Container within an Activity.
    """
    symbol: str
    measure: Measure
    text: str
    entity: Dependency


    def get_model (  # pylint: disable=W0102
        self,
        converter: Converter,
        *,
        prep_map: dict[ str, str ] = {},
        humanize: bool = True,  # pylint: disable=W0613
        pluralize: bool = True,  # pylint: disable=W0613
        ) -> dict:
        """
Serializable representation for JSON.
        """
        amount: str = self.measure.humanize()

        dat: dict = {
            "kind": "add",
            "subject": self.symbol,
            "amount": amount,
            "text": self.text,
        }

        if converter is not None:
            conv: str =  self.measure.convert(
                self.symbol,
                self.entity.external,
                converter,
            )

            if conv is not None and len(conv) > 0:
                dat["convert"] = conv

        if self.entity.external:
            dat["external"] = self.entity.external

        if self.symbol in prep_map:
            dat["url"] = prep_map[self.symbol]

        if self.note is not None:
            dat.update(self.note.get_model())

        return dat



class OpTransfer (OpGeneric):  # pylint: disable=R0902
    """
Represents the action to Transfer an intermediate product from one
Container into the Container used in a subsequent Activity, both
*within* the same Closure.
    """
    symbol: str
    entity: Dependency


    def get_model (  # pylint: disable=W0102
        self,
        converter: Converter,  # pylint: disable=W0613
        *,
        prep_map: dict[ str, str ] = {},  # pylint: disable=W0613
        humanize: bool = True,  # pylint: disable=W0613
        pluralize: bool = True,  # pylint: disable=W0613
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "kind": "transfer",
            "subject": self.symbol,
        }

        if self.note is not None:
            dat.update(self.note.get_model())

        return dat


class OpAction (OpGeneric):  # pylint: disable=R0902
    """
Represents the action of a Cook using a Tool to perform part of an
Activity on the food within a specific Container.
    """
    tool: Dependency
    modifier: str
    until: str
    duration: Duration
    product: Product | None = None


    def get_duration (  # type: ignore  # pylint: disable=W0221
        self,
        ) -> Duration:
        """
Duration of this operation.
        """
        return self.duration


    def get_model (
        self,
        *,
        humanize: bool = True,  # pylint: disable=W0613
        pluralize: bool = True,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "kind": "action",
            "subject": self.tool.symbol,
            "text": self.modifier,
            "until": self.until,
            "time": self.duration.humanize(pluralize = pluralize),
        }

        if self.product is not None:
            dat.update(self.product.get_model())

        if self.note is not None:
            dat.update(self.note.get_model())

        return dat


class OpWait (OpGeneric):  # pylint: disable=R0902
    """
Represents waiting for some time period or condition,
as part of an Activity on the food within a specific
Container.
    """
    modifier: str
    until: str
    duration: Duration
    product: Product | None = None


    def get_duration (  # type: ignore  # pylint: disable=W0221
        self,
        ) -> Duration:
        """
Duration of this operation.
        """
        return self.duration


    def get_model (
        self,
        *,
        humanize: bool = True,  # pylint: disable=W0613
        pluralize: bool = True,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "kind": "wait",
            "text": self.modifier,
            "until": self.until,
            "time": self.duration.humanize(pluralize = pluralize),
        }

        if self.product is not None:
            dat.update(self.product.get_model())

        if self.note is not None:
            dat.update(self.note.get_model())

        return dat


class OpAppliance (OpGeneric):  # pylint: disable=R0902
    """
Represents the process of an Appliance operating on the food within
a specific Container as part of an Activity.
    """
    container: Dependency
    modifier: str
    until: str
    duration: Duration
    product: Product | None = None
    appliance: str = Appliance.GENERIC
    verb: str = "generic"


    def get_duration (  # type: ignore  # pylint: disable=W0221
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
    verb: str = "heat"


    def get_model (
        self,
        *,
        humanize: bool = True,  # pylint: disable=W0613
        pluralize: bool = True,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "kind": self.verb,
            "subject": self.container.symbol,
            "text": self.modifier,
            "until": self.until,
            "time": self.duration.humanize(pluralize = pluralize),
        }

        if self.product is not None:
            dat.update(self.product.get_model())

        if self.note is not None:
            dat.update(self.note.get_model())

        return dat


class OpChill (OpHeat):  # pylint: disable=R0902
    """
Represents an Appliance: cooler --
used to *chill* in different modes.
    """
    appliance: str = Appliance.COOLER
    verb: str = "chill"


class OpBake (OpAppliance):  # pylint: disable=R0902
    """
Represents an Appliance: oven --
used to *bake* in different modes.
    """
    mode: str
    temperature: Temperature
    appliance: str = Appliance.OVEN
    verb: str = "bake"


    def get_model (
        self,
        *,
        humanize: bool = True,  # pylint: disable=W0613
        pluralize: bool = True,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "kind": self.verb,
            "subject": self.container.symbol,
            "text": self.modifier,
            "until": self.until,
            "time": self.duration.humanize(pluralize = pluralize),
            "mode": self.mode.lower(),
            "temperature": self.temperature.humanize(),
        }

        if self.product is not None:
            dat.update(self.product.get_model())

        if self.note is not None:
            dat.update(self.note.get_model())

        return dat


OpsTypes = typing.Union[
    OpAdd,
    OpTransfer,
    OpAction,
    OpWait,
    OpHeat,
    OpChill,
    OpBake,
]
