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
import typing

from icecream import ic  # pylint: disable=W0611
from PIL import Image
from pydantic import BaseModel
from upath import UPath
import requests
import requests_cache

from .measure import Converter, PLURAL, Product
from .ops import Dependency, DependencyDict, OpsTypes


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
## structural classes

class Ratio (BaseModel):  # pylint: disable=R0902
    """
A data class representing one Ratio object.
    """
    name: str
    formula: str
    parts: typing.Dict[ str, typing.List[ str ] ] = {}


    def get_model (
        self,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "name": self.name,
            "formula": self.formula,
            "parts": self.parts,
        }

        return dat


class Activity (BaseModel):  # pylint: disable=R0902
    """
A data class representing one Activity object.
    """
    container: Dependency
    text: str
    inputs: typing.List[ OpsTypes ] = []
    ops: typing.List[ OpsTypes ] = []


    def get_model (
        self,
        converter: Converter,
        *,
        humanize: bool = True,
        pluralize: bool = True,
        ) -> dict:
        """
Serializable representation for JSON.
        """
        dat: dict = {
            "container": self.container.symbol,
            "title": self.text,
            "uses": [
                op.get_model(converter, pluralize = pluralize)  # type: ignore
                for op in self.inputs
            ],
            "ops": [
                op.get_model(humanize = humanize, pluralize = pluralize)  # type: ignore
                for op in self.ops
            ],
        }

        return dat


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
    activities: typing.List[ Activity ] = []
    products: typing.List[ Product ] = []
    ratio: Ratio | None = None


    def total_yields (
        self,
        *,
        intermediaries: bool = False,
        ) -> typing.List[ str ]:
        """
Accessor for the total, non-intermediate yields of one Closure object.
        """
        yields_list: typing.List[ str ] = []

        for product in self.products:
            if intermediaries or not product.intermediate:
                amount: str = product.amount.humanize_convert(
                    product.symbol,
                    False,
                    None,
                )

                portions: str = "portion"

                if amount != "1":
                    portions = PLURAL.plural(portions)

                html: str = f"{amount} {portions} {product.symbol}".replace("_", " ").strip()
                yields_list.append(html)

        return yields_list


    def gen_rdf (
        self,
        global_ns: str,
        product_names: dict[ str, Product ],
        closure_urn: str,
        ) -> list[ str ]:
        """
Generate RDF modeling from OTTR templates.
        """
        rdf_data: list[ str ] = [f"""
bwyd:Closure(
  <{ closure_urn }> ,
  "{ self.name }"@en ,
  "{ self.text }"@en ,
) .
        """.strip()]

        for tag in self.supers:
            tag_urn: str = f"{ global_ns }:super:{ tag }"

            rdf_data.append(f"""
bwyd:ClosureSuper(
  <{ closure_urn }> ,
  <{ tag_urn }> ,
) .

bwyd:Super(
  <{ tag_urn }> ,
  "{ tag }"@en ,
) .
            """.strip())

        for tag in self.keywords:
            tag_urn = f"{ global_ns }:keyword:{ tag }"

            rdf_data.append(f"""
bwyd:ClosureKeyword(
  <{ closure_urn }> ,
  <{ tag_urn }> ,
) .

bwyd:Keyword(
  <{ tag_urn }> ,
  "{ tag }"@en ,
) .
            """.strip())

        for ingr_symbol in self.ingredients:
            if ingr_symbol in product_names:
                consumes_urn: str = product_names[ingr_symbol].urn
            else:
                consumes_urn = f"{ global_ns }:ingredient:{ ingr_symbol }"

            rdf_data.append(f"""
bwyd:ClosureConsumes(
  <{ closure_urn }> ,
  <{ consumes_urn }> ,
) .
            """.strip())

        for prod in self.products:
            label: str = prod.symbol.replace("_", " ")

            if prod.intermediate:
                produces_urn: str = f"{ closure_urn }:product:{ prod.symbol }"

                rdf_data.append(f"""
bwyd:ClosureProduces(
  <{ closure_urn }> ,
  <{ produces_urn }> ,
  "{ label }"@en ,
) .
                """.strip())

            else:
                produces_urn = f"{ global_ns }:product:{ prod.symbol }"

                rdf_data.append(f"""
bwyd:ClosureProduces(
  <{ closure_urn }> ,
  <{ produces_urn }> ,
  "{ label }"@en ,
) .
bwyd:Product(
  <{ produces_urn }> ,
  "{ label }"@en ,
) .
                """.strip())

        return rdf_data
