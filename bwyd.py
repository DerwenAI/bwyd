#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
"""

from collections import OrderedDict
import json
import pathlib
import typing

from icecream import ic
import textx


class Bwyd:
    """
Parse and interpret the Bwyd language.
    """

    def __init__ (
        self,
        ) -> None:
        """
Constructor.
        """
        self.equipment: typing.Dict[ str, str ] = OrderedDict()
        self.ingredients: typing.Dict[ str, str ] = OrderedDict()


    def as_json (
        self,
        ) -> dict:
        """
Return a JSON-friendly dictionary representation.
        """
        return {
            "equipment": self.equipment,
            "ingredients": self.ingredients,
        }


    def interpret_closure (
        self,
        closure,
        *,
        debug: bool = False,
        ) -> None:
        """
Process interpreter for one Closure.
        """
        for cmd in closure.commands:
            if debug:
                ic(cmd)

            match cmd.__class__.__name__:
                case "Container":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    self.equipment[cmd.symbol] = cmd.text

                case "Focus":
                    if debug:
                        ic(cmd.symbol)

                    if cmd.symbol not in self.equipment:
                        print(f"CONTAINER: {cmd.symbol} not found")

                case "Tool":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    self.equipment[cmd.symbol] = cmd.text

                case "Action":
                    if debug:
                        ic(cmd.symbol, cmd.modifier, cmd.until, cmd.time)

                    if cmd.symbol not in self.equipment:
                        print(f"TOOL: {cmd.symbol} not found")

                case "Ingredient":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    self.ingredients[cmd.symbol] = cmd.text

                case "Ratio":
                    if debug:
                        ic(cmd.name, [ (e.name, e.components) for e in cmd.elements ])

                case "Add":
                    if debug:
                        ic(cmd.symbol, cmd.quantity, cmd.modifier)

                    if cmd.symbol not in self.ingredients:
                        print(f"INGREDIENT: {cmd.symbol} not found")

                case "Note":
                    if debug:
                        ic(cmd.text)


    def interpret_program (
        self,
        program,
        *,
        debug: bool = False,
        ) -> None:
        """
Process interpreter for once instance of a Bwyd program.
        """
        for closure in program.closures:
            self.interpret_closure(
                closure,
                debug = debug,
            )


if __name__ == "__main__":
    bwyd_mm: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        "bwyd.tx",
        debug = False, # True
    )

    # parse a program

    program_file: pathlib.Path = pathlib.Path("prog.bwyd")
    parsed_program = bwyd_mm.model_from_file(
        program_file,
        debug = False, # True
    )

    # interpret the parsed program

    bwyd: Bwyd = Bwyd()
    bwyd.interpret_program(
        parsed_program,
        debug = False, # True
    )

    # make a summary report

    print(json.dumps(
        bwyd.as_json(),
        indent = 2,
        sort_keys = True,
    ))
