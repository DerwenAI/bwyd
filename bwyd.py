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
        for cmd in closure.commands:
            ic(cmd)

            match cmd.__class__.__name__:
                case "Ratio":
                    ic(cmd.name, cmd.components)
                case "Note":
                    ic(cmd.text)
                case "Container":
                    ic(cmd.symbol, cmd.text)
                case "Ingredient":
                    ic(cmd.symbol, cmd.text)
                case "Focus":
                    ic(cmd.symbol)
                case "Add":
                    ic(cmd.symbol, cmd.quantity, cmd.modifier)
                case "Tool":
                    ic(cmd.symbol, cmd.text)
                case "Action":
                    ic(cmd.symbol, cmd.modifier, cmd.until, cmd.time)


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

    program_file: pathlib.Path = pathlib.Path("prog.bwyd")

    bwyd_program = bwyd_mm.model_from_file(
        program_file,
        debug = False, # True
    )

    bwyd: Bwyd = Bwyd()
    bwyd.interpret_program(bwyd_program)
