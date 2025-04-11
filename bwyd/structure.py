#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from dataclasses import dataclass, field
from urllib.parse import urlparse
import itertools
import typing

from upath import UPath

from .measure import Measure

from .ops import Dependency, DependencyDict, \
    OpsTypes, OpAdd


######################################################################
## gallery classes

@dataclass(order = False, frozen = False)
class Post:  # pylint: disable=R0902
    """
A data class representing one Post object.
    """
    url: str


    def get_image (
        self,
        ) -> str:
        """
Accessor for an embeddable URL.
        """
        host: typing.Optional[ str ] = urlparse(self.url).hostname

        if host and host.endswith(".instagram.com"):
            embed: UPath = UPath(self.url) / "embed"
            return embed.as_posix()

        return self.url


    def get_thumbnail (
        self,
        ) -> str:
        """
Accessor for a thumbnail URL.
        """
        host: typing.Optional[ str ] = urlparse(self.url).hostname

        if host and host.endswith(".instagram.com"):
            embed: UPath = UPath(self.url) / "media" / "?size=l"
            return embed.as_posix()

        return self.url


######################################################################
## yields classes

@dataclass(order = False, frozen = False)
class Product:  # pylint: disable=R0902
    """
A data class representing one Product object.
    """
    loc: dict
    symbol: str
    amount: Measure
    intermediate: bool
    ref_count: int = 0


######################################################################
## structural classes

@dataclass(order = False, frozen = False)
class Activity:  # pylint: disable=R0902
    """
A data class representing one Activity object.
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
    text: str = ""
    containers: DependencyDict = field(default_factory = lambda: DependencyDict())  # pylint: disable=W0108
    tools: DependencyDict = field(default_factory = lambda: DependencyDict())  # pylint: disable=W0108
    ingredients: DependencyDict = field(default_factory = lambda: DependencyDict())  # pylint: disable=W0108
    foci: typing.List[ Focus ] = field(default_factory = lambda: [])
    products: typing.List[ Product ] = field(default_factory = lambda: [])


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

    def total_yields (
        self,
        *,
        intermediaries: bool = False,
        ) -> typing.List[ str ]:
        """
Accessor for the total, non-intermediate yields of one Closure object.
        """
        return [
            f"{product.amount.humanize().strip()} {product.symbol}".replace("_", " ")
            for product in self.products
            if intermediaries or not product.intermediate
        ]
