#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
from dataclasses import dataclass, field
from fractions import Fraction
import itertools
import typing

from icecream import ic


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
            "symbol": self.symbol,
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
## measures

@dataclass(order = False, frozen = False)
class Measure:  # pylint: disable=R0902
    """
A data class representing one parsed Measure object.
    """
    amount: float
    units: str

    def humanize (
        self
        ) -> str:
        """
Denormalize this measure into human-readable form.
        """
        html: str = f"{self.amount} "

        if self.units is not None:
            html += self.units

        return html


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "amount": self.amount,
            "units": self.units,
        }


@dataclass(order = False, frozen = False)
class Duration (Measure):  # pylint: disable=R0902
    """
A data class representing one parsed Duration object.
    """

    def normalize (
        self,
        ) -> int:
        """
Return this duration normalized into seconds.
        """
        norm_ratio: typing.Dict[ str, int ] = {
            "sec": 1,
            "min": 60,
            "hrs": 3600,
        }

        return self.amount * norm_ratio[self.units]


    def humanize (
        self,
        ) -> str:
        """
Denormalize this duration into human-readable form.
        """
        amount: int = int(self.amount)
        readable: str = f"{amount:d} {self.units}"

        if self.units == "min":
            if self.amount > 60:
                hrs_amount: int = int(self.amount / 60)
                min_remain: int = int(self.amount % 60)
                readable = f"{hrs_amount:d} hrs, {min_remain} min"

        elif self.units == "sec":
            if self.amount > 3600:
                hrs_amount: int = int(self.amount / 3600)
                min_remain: int = self.amount % 3600
                min_amount: int = int(min_remain / 60)
                sec_remain: int = int(min_remain % 60)
                readable = f"{hrs_amount:d} hrs, {min_amount:d} min, {sec_remain:d} sec"
            elif self.amount > 60:
                min_amount: int = int(self.amount / 60)
                sec_remain: int = int(self.amount % 60)
                readable = f"{min_amount:d} min, {sec_remain:d} sec"

        return readable


    def get_model (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "amount": self.amount,
            "units": self.units,
        }


@dataclass(order = False, frozen = False)
class Temperature (Measure):  # pylint: disable=R0902
    """
A data class representing one parsed Temperature object.
    """

    def humanize (
        self
        ) -> str:
        """
HTML represenation.
        """
        html: str = f"{self.amount} °{self.units}"

        if self.units == "C":
            f_deg: int = int(
                round( ((self.amount / 5.0 * 9.0) + 32.0) / 5.0) * 5.0
            )

            html += f" ({f_deg} °F)"

        return html


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
        ) -> str:
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


    @classmethod
    def humanize_cup (
        cls,
        amount: float,
        ) -> str:
        """
Humanize imperial measurement ratios, for cups
        """
        units: str = "cup"
        denom_limit: int = 4

        if amount <= 0.24:
            return cls.humanize_tsp(amount * 16.0)
        elif amount >= 1.0:
            human: str = cls.humanize_ratio(amount)
            #human: str = f"{round(amount, 2):.2f}"
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        return f"{human} {units}"
    

    @classmethod
    def humanize_tsp (
        cls,
        amount: float,
        ) -> str:
        """
Humanize imperial measurement ratios, for cups
        """
        units: str = "tsp"
        denom_limit: int = 8

        if amount >= 0.95:
            human: str = cls.humanize_ratio(amount)
            #human: str = f"{round(amount, 2):.2f}"
        elif amount >= 0.4:
            human = str(Fraction(round(amount, 1)).limit_denominator(denom_limit))
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        return f"{human} {units}"


    @classmethod
    def humanize_ratio (
        cls,
        amount: float,
        ) -> str:
        """
Humanize imperial measurement ratios >= 1.0
        """
        base: int = int(amount)
        frac: float = amount - float(base)

        if frac < 0.2:
            return str(base)

        denom_limit: int = 4
        human = str(Fraction(round(frac, 2)).limit_denominator(denom_limit))

        return f"{base:d} {human}"


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
            imper_units, metric_units, ratio = converter[self.symbol]

            if self.measure.units == metric_units:
                imper_amount: float = self.measure.amount / ratio
                amount += f" ({self.humanize_cup(imper_amount)})"

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
        ) -> str:
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
        ) -> str:
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
        ) -> str:
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
