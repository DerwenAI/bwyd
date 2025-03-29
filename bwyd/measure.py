#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Measurement objects in the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from dataclasses import dataclass, field
from fractions import Fraction
import typing


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
