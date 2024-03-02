#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
from dataclasses import dataclass, field
import typing


######################################################################
## language object definitions

@dataclass(order=False, frozen=False)
class Measure:  # pylint: disable=R0902
    """
A data class representing one parsed Measure object.
    """
    amount: float
    units: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "amount": self.amount,
            "units": self.units,
        }


@dataclass(order=False, frozen=False)
class Duration:  # pylint: disable=R0902
    """
A data class representing one parsed Duration object.
    """
    amount: float
    units: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "amount": self.amount,
            "units": self.units,
        }


@dataclass(order=False, frozen=False)
class OpAdd:  # pylint: disable=R0902
    """
A data class representing one Add object.
    """
    symbol: str
    measure: Measure
    text: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "op": "add",
            "symbol": self.symbol,
            "measure": self.measure.to_json(),
            "text": self.text,
        }


@dataclass(order=False, frozen=False)
class OpUse:  # pylint: disable=R0902
    """
A data class representing one Use object.
    """
    symbol: str
    name: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "op": "use",
            "symbol": self.symbol,
            "name": self.name,
        }


@dataclass(order=False, frozen=False)
class OpAction:  # pylint: disable=R0902
    """
A data class representing one Action object.
    """
    tool: str
    modifier: str
    until: str
    duration: Duration

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "op": "action",
            "tool": self.tool,
            "modifier": self.modifier,
            "until": self.until,
            "duration": self.duration.to_json(),
        }


@dataclass(order=False, frozen=False)
class OpChill:  # pylint: disable=R0902
    """
A data class representing one Chill object.
    """
    container: str
    modifier: str
    until: str
    duration: Duration

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "op": "chill",
            "container": self.container,
            "modifier": self.modifier,
            "until": self.until,
            "duration": self.duration.to_json(),
        }


OpsTypes = typing.Union[ OpAdd, OpUse, OpAction, OpChill ]


@dataclass(order=False, frozen=False)
class Focus:  # pylint: disable=R0902
    """
A data class representing a parsed Focus object.
    """
    container: str
    ops: typing.List[ OpsTypes ] = field(default_factory = lambda: [])

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "container": self.container,
            "ops": [ op.to_json() for op in self.ops ],
        }


@dataclass(order=False, frozen=False)
class Closure:  # pylint: disable=R0902
    """
A data class representing one parsed Closure object.
    """
    name: str
    obj: typing.Any
    yields: Measure
    notes: typing.List[ str ] = field(default_factory = lambda: [])
    tools: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())  # pylint: disable=W0108
    containers: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())  # pylint: disable=W0108
    ingredients: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())  # pylint: disable=W0108
    foci: typing.List[ Focus ] = field(default_factory = lambda: [])
    active_focus: typing.Optional[ Focus ] = None

    def focus_op (
        self,
        cmd: typing.Any,
        op_obj: OpsTypes,
        ) -> None:
        """
Append one operation to the active Focus.
        """
        if self.active_focus is None:
            print(f"FOCUS: not defined yet for {cmd.symbol}")
        else:
            self.active_focus.ops.append(op_obj)
