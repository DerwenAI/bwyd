#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Measurement objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
from fractions import Fraction
import logging
import typing

from icecream import ic  # type: ignore  # pylint: disable=W0611
from pydantic import BaseModel, NonNegativeFloat, PositiveFloat
import inflect


PLURAL = inflect.engine()

NORM_RATIO: typing.Dict[ str, int ] = OrderedDict({
    "year": 60 * 60 * 24 * 365,
    "month": 60 * 60 * 24 * 30,
    "day": 60 * 60 * 24,
    "hour": 60 * 60,
    "minute": 60,
    "second": 1,
})

CUPS_PER_LITER: float = 4.226753
POUNDS_PER_GRAM: float = 0.002204623


class Conversion (BaseModel):  # pylint: disable=R0902
    """
A data class representing one Conversion object.
    """
    symbol: str
    density: PositiveFloat
    imperial: str = "cup"
    metric: str = "g"


Converter = typing.Dict[ str, Conversion ]


class Measure (BaseModel):  # pylint: disable=R0902
    """
A data class representing one parsed Measure object.
    """
    amount: NonNegativeFloat
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


    def humanize_convert (
        self,
        symbol: str,
        external: bool,
        converter: Converter,
        ) -> str:
        """
Denormalize this measure into human-readable form, with an
imperial conversion if available.
        """
        amount: str = self.humanize().strip()

        if symbol in converter:
            conv: Conversion = converter[symbol]

            if self.units == conv.metric:
                imper_amount: float = self.amount / conv.density
                amount += f" ({self.humanize_cup(imper_amount)})"

        elif self.units is not None:
            if not external:
                logging.warning(f"no conversion ratio for {symbol}")  # pylint: disable=W1203

            match self.units:
                case "g":
                    imper_amount = self.amount * POUNDS_PER_GRAM
                    amount += self.humanize_generic(imper_amount, "pounds")

                case "l":
                    imper_amount = self.amount * CUPS_PER_LITER
                    amount += self.humanize_generic(imper_amount, "cups")

                case _:
                    logging.warning(f"no default conversion for unit `{self.units}`")  # pylint: disable=W1203

        return amount


    @classmethod
    def humanize_generic (
        cls,
        amount: float,
        units: str,
        ) -> str:
        """
Humanize imperial measurement ratios, for generic case
        """
        denom_limit: int = 4

        if amount > .95:
            human: str = cls.humanize_ratio(amount)
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        return f" ({human} {units})"


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

        if amount >= 1.0:
            human: str = cls.humanize_ratio(amount)
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        if amount > 1.0:
            units = PLURAL.plural(units)

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
        elif amount >= 0.4:
            human = str(Fraction(round(amount, 1)).limit_denominator(denom_limit))
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        if amount > 1.0:
            units = PLURAL.plural(units)

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

        if frac >= 0.9:
            return str(round(amount))
        if frac < 0.2:
            return str(base)

        denom_limit: int = 4
        human = str(Fraction(round(frac, 2)).limit_denominator(denom_limit))

        return f"{base:d} {human}"


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


class Duration (Measure):  # pylint: disable=R0902
    """
A data class representing one parsed Duration object.
    """
    def normalize (
        self,
        ) -> float:
        """
Return this duration normalized into seconds.
        """
        return self.amount * NORM_RATIO[self.units]


    def humanize (
        self,
        ) -> str:
        """
Adapted from:
<https://stackoverflow.com/a/56499010/1698443>
        """
        (years, remainder) = divmod(self.normalize(), 31536000)
        (months, remainder) = divmod(remainder, 2592000)
        (days, remainder) = divmod(remainder, 86400)
        (hours, remainder) = divmod(remainder, 3600)
        (minutes, seconds) = divmod(remainder, 60)

        cascade: zip = zip(
            NORM_RATIO.keys(),
            ( years, months, days, hours, minutes, seconds, ),
        )

        units: list = []

        for label, amount in cascade:
            if amount > 0:
                if amount > 1:
                    label = PLURAL.plural(label)

                units.append(f"{int(amount)} {label}")

        readable: str = ", ".join(units)
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


class Temperature (Measure):  # pylint: disable=R0902
    """
A data class representing one parsed Temperature object.
    """
    def humanize (
        self
        ) -> str:
        """
HTML representation.
        """
        html: str = f"{self.amount} °{self.units}"

        if self.units == "C":
            f_deg: int = int(
                round( ((self.amount / 5.0 * 9.0) + 32.0) / 5.0) * 5.0
            )

            html += f" ({f_deg} °F)"

        return html
