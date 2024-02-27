#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
"""

import pathlib

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
        # initial position is (0,0)
        self.x = 0
        self.y = 0


    def __str__ (
        self,
        ) -> str:
        """
String representation.
        """
        return f"position {self.x}, {self.y}."


    def interpret_closure (
        self,
        closure,
        ) -> None:
        """
Process interpreter for one Closure.
        """
        for command in closure.commands:
            ic(command)

            match command.__class__.__name__:
                case "Ratio":
                    print("ratio")
                case "Note":
                    ic(command.text)
                case "Ingredient":
                    ic(command.symbol, command.text)
                case "Tool":
                    ic(command.symbol, command.text)
                case "Add":
                    ic(command.symbol, command.modifier)


    def interpret_program (
        self,
        program,
        ) -> None:
        """
Process interpreter for once instance of a Bwyd program.
        """
        for closure in program.closures:
            self.interpret_closure(closure)


if __name__ == "__main__":
    bwyd_mm: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        "bwyd.tx",
        debug = False, # True
    )

    program_file: pathlib.Path = pathlib.Path("program.bwyd")

    bwyd_program = bwyd_mm.model_from_file(
        program_file,
        debug = False, # True
    )

    bwyd: Bwyd = Bwyd()
    bwyd.interpret_program(bwyd_program)
