#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
"""

from collections import OrderedDict
from dataclasses import dataclass, field
import json
import pathlib
import typing

from icecream import ic
import textx


######################################################################
## class definitions                                                                                                                        

@dataclass(order=False, frozen=False)
class Closure:  # pylint: disable=R0902                                                                                                  
    """
A data class representing one parsed Closure object.
    """
    name: str
    obj: typing.Any
    equipment: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())
    ingredients: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())


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
        self.closures: typing.Dict[ str, Closure ] = {}


    def as_json (
        self,
        ) -> typing.List[dict]:
        """
Return a list of JSON-friendly dictionary representations, one for
each parsed Closure.
        """
        return [
            {
                "name": name,
                "equipment": clos_obj.equipment,
                "ingredients": clos_obj.ingredients,
            }
            for name, clos_obj in self.closures.items()
        ]


    def interpret_closure (
        self,
        closure,
        *,
        debug: bool = False,
        ) -> Closure:
        """
Process interpreter for one Closure.
        """
        clos_obj: Closure = Closure(
            name = closure.name,
            obj = closure,
        )

        for cmd in closure.commands:
            if debug:
                #ic(dir(closure))
                ic(cmd)

            match cmd.__class__.__name__:
                case "Container":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    clos_obj.equipment[cmd.symbol] = cmd.text

                case "Focus":
                    if debug:
                        ic(cmd.symbol)

                    if cmd.symbol not in clos_obj.equipment:
                        print(f"CONTAINER: {cmd.symbol} not found")

                case "Tool":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    clos_obj.equipment[cmd.symbol] = cmd.text

                case "Action":
                    if debug:
                        ic(cmd.symbol, cmd.modifier, cmd.until, cmd.time)

                    if cmd.symbol not in clos_obj.equipment:
                        print(f"TOOL: {cmd.symbol} not found")

                case "Ingredient":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    clos_obj.ingredients[cmd.symbol] = cmd.text

                case "Ratio":
                    if debug:
                        ic(cmd.name, [ (e.name, e.components) for e in cmd.elements ])

                case "Add":
                    if debug:
                        ic(cmd.symbol, cmd.quantity, cmd.modifier)

                    if cmd.symbol not in clos_obj.ingredients:
                        print(f"INGREDIENT: {cmd.symbol} not found")

                case "Use":
                    if debug:
                        ic(cmd.symbol, cmd.name)

                    clos_obj.ingredients[cmd.symbol] = cmd.name

                    if cmd.name not in self.closures:
                        print(f"CLOSURE: {cmd.name} not found")

                case "Note":
                    if debug:
                        ic(cmd.text)

        return clos_obj


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
            self.closures[closure.name] = self.interpret_closure(
                closure,
                debug = debug,
            )


if __name__ == "__main__":
    bwyd_mm: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        "bwyd.tx",
        debug = False, # True
    )

    ## parse a program
    program_file: pathlib.Path = pathlib.Path("prog.bwyd")
    parsed_program = bwyd_mm.model_from_file(
        program_file,
        debug = False, # True
    )

    ## interpret the parsed program
    bwyd: Bwyd = Bwyd()
    bwyd.interpret_program(
        parsed_program,
        debug = True, # False
    )

    ## make a summary report
    print(json.dumps(
        bwyd.as_json(),
        indent = 2,
        sort_keys = False,
    ))
