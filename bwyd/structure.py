#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from urllib.parse import urlparse
import base64
import io
import logging
import itertools
import typing

from PIL import Image
from pydantic import BaseModel, NonNegativeInt
from upath import UPath
import requests
import requests_cache

from .measure import Measure, Converter

from .ops import Dependency, DependencyDict, \
    OpsTypes, OpAdd


######################################################################
## gallery classes

class Post (BaseModel):  # pylint: disable=R0902
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


    def thumbify (
        self,
        img_url: str,
        session: requests_cache.CachedSession,
        ) -> str:
        """
Access an image by URL, resize to thumbnail, convert to a data URL.
        """
        data_url: str = img_url

        try:
            req: requests_cache.CachedResponse = session.get(  # type: ignore
                img_url,
                timeout = 10,
                stream = True,
            )

            image: Image = Image.open(req.raw)  # type: ignore

            max_size: typing.Tuple[ int, int ] = (50, 50,)
            image.thumbnail(max_size)  # type: ignore

            buffered: io.BytesIO = io.BytesIO()
            image.save(buffered, format = "JPEG")  # type: ignore

            hex_data: str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            data_url = f"data:image/jpeg;base64,{hex_data}"

        except requests.exceptions.Timeout as ex:  # pylint: disable=W0612
            error_msg: str = f"URL read timeout: {img_url}"
            logging.error(error_msg)

        return data_url


    def get_thumbnail (
        self,
        session: requests_cache.CachedSession,
        ) -> str:
        """
Accessor for a thumbnail URL.
        """
        host: typing.Optional[ str ] = urlparse(self.url).hostname

        if host and host.endswith(".instagram.com"):
            embed: UPath = UPath(self.url) / "media" / "?size=l"
            return self.thumbify(embed.as_posix(), session)

        return self.url


######################################################################
## yields classes

class Product (BaseModel):  # pylint: disable=R0902
    """
A data class representing one Product object.
    """
    loc: dict
    symbol: str
    amount: Measure
    intermediate: bool
    ref_count: NonNegativeInt = 0


######################################################################
## structural classes

class Activity (BaseModel):  # pylint: disable=R0902
    """
A data class representing one Activity object.
    """
    text: str
    ops: typing.List[ OpsTypes ] = []


    def get_model (
        self,
        converter: Converter,
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


class Focus (BaseModel):  # pylint: disable=R0902
    """
A data class representing a parsed Focus object.
    """
    container: Dependency
    activities: typing.List[ Activity ] = []


    def get_model (
        self,
        converter: Converter,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "container": self.container.symbol,
            "activities": [ act.get_model(converter) for act in self.activities ],
        }


class Closure (BaseModel, arbitrary_types_allowed = True):  # pylint: disable=R0902
    """
A data class representing one parsed Closure object.
    """
    name: str
    obj: typing.Any
    text: str = ""
    supers: typing.List[ str ] = []
    keywords: typing.List[ str ] = []
    containers: DependencyDict = DependencyDict()
    tools: DependencyDict = DependencyDict()
    ingredients: DependencyDict = DependencyDict()
    foci: typing.List[ Focus ] = []
    products: typing.List[ Product ] = []


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
