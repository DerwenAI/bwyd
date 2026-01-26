#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Measurement objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
from fractions import Fraction
import enum
import logging
import typing

from icecream import ic  # type: ignore  # pylint: disable=W0611
from pydantic import BaseModel, NonNegativeFloat, PositiveFloat
import inflect


class MeasureUnits (enum.StrEnum):
    """
An enumeration class representing string literals for Measure units.
    """
    TEASPOON = "tsp"
    CUP = enum.auto()
    POUND = enum.auto()
    OUNCE = enum.auto()
    LITER = "l"
    MILLILITER = "ml"
    GRAM = "g"
    KILOGRAM = "kg"

OUNCE_PER_POUND: float = 16.0
CUP_PER_LITER: float = 4.226753
POUND_PER_GRAM: float = 0.002204623


class DurationUnits (enum.StrEnum):
    """
An enumeration class representing string literals for Duration units.
    """
    SECOND = enum.auto()
    MINUTE = enum.auto()
    HOUR = enum.auto()
    DAY = enum.auto()
    MONTH = enum.auto()
    YEAR = enum.auto()


NORM_RATIO: typing.Dict[ str, int ] = OrderedDict({
    DurationUnits.YEAR.value: 60 * 60 * 24 * 365,
    DurationUnits.MONTH.value: 60 * 60 * 24 * 30,
    DurationUnits.DAY.value: 60 * 60 * 24,
    DurationUnits.HOUR.value: 60 * 60,
    DurationUnits.MINUTE.value: 60,
    DurationUnits.SECOND.value: 1,
})


class TemperatureUnits (enum.StrEnum):
    """
An enumeration class representing string literals for Temperature units.
    """
    CELSIUS = "C"
    FAHRENHEIT = "F"


PLURAL = inflect.engine()


class Conversion (BaseModel):  # pylint: disable=R0902
    """
A data class representing one Conversion object.
    """
    symbol: str
    density: PositiveFloat
    imperial: str = MeasureUnits.CUP.value
    metric: str = MeasureUnits.GRAM.value


Converter = typing.Dict[ str, Conversion ]


class Humanized (BaseModel):  # pylint: disable=R0902
    """
A data class representing one humanized Measure object.
    """
    amount: NonNegativeFloat
    human: str
    units: typing.Optional[ MeasureUnits ]


    def denormalize (
        self
        ) -> str:
        """
Denormalize a meaure which is already in human-readable form.
        """
        if self.units is None:
            return f" ({self.human})"

        units: str = self.units.value

        if self.amount > 1.0 and self.human != "1" and self.units != MeasureUnits.TEASPOON:
            units = PLURAL.plural(units)

        return f" ({self.human} {units})"


class Measure (BaseModel):  # pylint: disable=R0902
    """
A data class representing one parsed Measure object.
    """
    amount: NonNegativeFloat
    units: typing.Optional[ str ]


    @classmethod
    def build (
        cls,
        parse: typing.Any,
        ) -> "Measure":
        """
Constructor from a `textx` parse object.
        """
        measure_units: typing.Optional[ str ] = None

        if parse.units is not None:
            measure_units = MeasureUnits(parse.units).value

        return Measure(
            amount = float(parse.amount),
            units = measure_units,
        )


    def humanize (
        self
        ) -> str:
        """
Denormalize this measure into human-readable form.
        """
        html: str = f"{self.amount}"

        if html.endswith(".0"):
            html = html[:-2]

        if self.units is not None:
            html = f"{html} {self.units}"

        return html


    def humanize_convert (
        self,
        symbol: str,
        external: bool,
        converter: typing.Optional[ Converter ],
        ) -> str:
        """
Denormalize this measure into human-readable form, with an
imperial conversion if available.
        """
        amount: str = self.humanize().strip()

        if converter is not None:
            if symbol in converter:
                conv: Conversion = converter[symbol]

                if self.units == conv.metric:
                    imper_amount: float = self.amount / conv.density
                    human: Humanized = self._humanize_cup(imper_amount)
                    amount += human.denormalize()

            elif self.units is not None:
                if not external:
                    logging.warning(f"no conversion ratio for {symbol}")  # pylint: disable=W1203

                match self.units:
                    case MeasureUnits.GRAM.value:
                        imper_amount = self.amount * POUND_PER_GRAM

                        if imper_amount < 0.25:
                            imper_amount *= OUNCE_PER_POUND
                            human = self._humanize_generic(imper_amount, MeasureUnits.OUNCE)
                        else:
                            human = self._humanize_generic(imper_amount, MeasureUnits.POUND)

                        amount += human.denormalize()
                    case MeasureUnits.LITER.value:
                        imper_amount = self.amount * CUP_PER_LITER
                        human = self._humanize_generic(imper_amount, MeasureUnits.CUP)
                        amount += human.denormalize()

                    case _:
                        logging.warning(f"no default conversion for unit `{self.units}`")  # pylint: disable=W1203

        return amount


    @classmethod
    def _humanize_generic (
        cls,
        amount: float,
        units: MeasureUnits,
        ) -> Humanized:
        """
Private method to humanize imperial measurement ratios, for generic case.
        """
        denom_limit: int = 4

        if amount > .95:
            human: str = cls.fix_fraction(amount)
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        return Humanized(
            amount = amount,
            human = human,
            units = units,
        )


    @classmethod
    def _humanize_cup (
        cls,
        amount: float,
        ) -> Humanized:
        """
Private method to humanize imperial measurement ratios, for cup.
        """
        units: MeasureUnits = MeasureUnits.CUP
        denom_limit: int = 4

        if amount <= 0.24:
            return cls._humanize_tsp(amount * 16.0)

        if amount >= 1.0:
            human: str = cls.fix_fraction(amount)
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        return Humanized(
            amount = amount,
            human = human,
            units = units,
        )


    @classmethod
    def _humanize_tsp (
        cls,
        amount: float,
        ) -> Humanized:
        """
Private method to humanize imperial measurement ratios, for teaspoon.
        """
        units: MeasureUnits = MeasureUnits.TEASPOON
        denom_limit: int = 8

        if amount >= 0.95:
            human: str = cls.fix_fraction(amount)
        elif amount >= 0.4:
            human = str(Fraction(round(amount, 1)).limit_denominator(denom_limit))
        else:
            human = str(Fraction(round(amount, 2)).limit_denominator(denom_limit))

        # plural for teaspoons is too easily confused with tablespoon

        return Humanized(
            amount = amount,
            human = human,
            units = units,
        )


    @classmethod
    def fix_fraction (
        cls,
        amount: float,
        ) -> str:
        """
Humanize fractions representing imperial measurement ratios >= 1.0
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


    @classmethod
    def build (
        cls,
        parse: typing.Any,
        ) -> "Duration":
        """
Constructor from a `textx` parse object.
        """
        duration_units: typing.Optional[ str ] = None

        if parse.units is not None:
            duration_units = DurationUnits(parse.units).value

        return Duration(
            amount = float(parse.amount),
            units = duration_units,
        )


    def normalize (
        self,
        ) -> float:
        """
Return this duration normalized into seconds.
        """
        return self.amount * float(NORM_RATIO[self.units])  # type: ignore


    def humanize (
        self,
        ) -> str:
        """
Adapted from:
<https://stackoverflow.com/a/56499010/1698443>
        """
        (years, remainder) = divmod(self.normalize(), NORM_RATIO[DurationUnits.YEAR.value])
        (months, remainder) = divmod(remainder, NORM_RATIO[DurationUnits.MONTH.value])
        (days, remainder) = divmod(remainder, NORM_RATIO[DurationUnits.DAY.value])
        (hours, remainder) = divmod(remainder, NORM_RATIO[DurationUnits.HOUR.value])
        (minutes, seconds) = divmod(remainder, NORM_RATIO[DurationUnits.MINUTE.value])

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

    @classmethod
    def build (
        cls,
        parse: typing.Any,
        ) -> "Temperature":
        """
Constructor from a `textx` parse object.
        """
        temperature_units: typing.Optional[ str ] = None

        if parse.units is not None:
            temperature_units = TemperatureUnits(parse.units).value

        return Temperature(
            amount = float(parse.amount),
            units = temperature_units,
        )


    @classmethod
    def celsius_to_fahrenheit (
        cls,
        amount: float,
        ) -> float:
        """
Convert from Celsius to Fahrenheit scale.
        """
        return (amount / 5.0 * 9.0) + 32.0


    @classmethod
    def fahrenheit_to_celsius (
        cls,
        amount: float,
        ) -> float:
        """
Convert from Fahrenheit to Celsius scale.
        """
        return (amount - 32.0) / 9.0 * 5.0


    def humanize (
        self
        ) -> str:
        """
HTML representation.
        """
        html: str = f"{self.amount} °{self.units}"

        if self.units == TemperatureUnits.CELSIUS.value:
            fahr: float = self.celsius_to_fahrenheit(self.amount)

            # round the converted temperature to the nearest 5 °F
            f_deg: int = int(round(fahr / 5.0) * 5.0)

            html += f" ({f_deg} °{TemperatureUnits.FAHRENHEIT.value})"

        return html
