#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import pathlib
import typing

from icecream import ic  # pylint: disable=E0401
import textx  # pylint: disable=E0401

from .objects import Duration, Measure, \
    OpAction, OpAdd, OpUse, \
    Closure, Focus


######################################################################
## parser/interpreter definitions

class Bwyd:
    """
Bwyd DSL parser/interpreter.
    """
    GRAMMAR: pathlib.Path = pathlib.Path(__file__).resolve().parent / "resources" / "bwyd.tx"

    META_MODEL: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        GRAMMAR,
        debug = False, # True
    )


    def __init__ (
        self,
        ) -> None:
        """
Constructor.
        """
        self.closures: typing.Dict[ str, Closure ] = {}


    def to_json (
        self,
        ) -> typing.List[dict]:
        """
Return a list of JSON-friendly dictionary representations,
one for each parsed Closure.
        """
        return [
            {
                "name": name,
                "yields": clos_obj.yields.to_json(),
                "notes": clos_obj.notes,
                "tools": clos_obj.tools,
                "containers": clos_obj.containers,
                "ingredients": clos_obj.ingredients,
                "foci": [ focus.to_json() for focus in clos_obj.foci ],
            }
            for name, clos_obj in self.closures.items()
        ]


    def parse (
        self,
        script: pathlib.Path,
        *,
        debug: bool = False,
        ) -> typing.Any:
        """
Parse one script.
        """
        return self.META_MODEL.model_from_file(
            script,
            debug = debug,
        )


    def interpret_closure (  # pylint: disable=R0912,R0915
        self,
        closure: typing.Any,
        *,
        debug: bool = False,
        ) -> Closure:
        """
Process interpreter for one Closure.
        """
        clos_obj: Closure = Closure(
            name = closure.name,
            obj = closure,
            yields = Measure(
                amount = closure.yields.amount,
                units = closure.yields.units,
            ),
        )

        for cmd in closure.commands:
            if debug:
                #ic(dir(closure))
                ic(cmd)

            cmd_class_name: str = cmd.__class__.__name__

            if cmd_class_name == "Container":
                if debug:
                    ic(cmd.symbol, cmd.text)

                clos_obj.containers[cmd.symbol] = cmd.text

            elif cmd_class_name == "Focus":
                if debug:
                    ic(cmd.symbol)

                if cmd.symbol not in clos_obj.containers:
                    print(f"CONTAINER: {cmd.symbol} not found")

                clos_obj.active_focus = Focus(
                    symbol = cmd.symbol,
                )

                clos_obj.foci.append(clos_obj.active_focus)

            elif cmd_class_name == "Tool":
                if debug:
                    ic(cmd.symbol, cmd.text)

                clos_obj.tools[cmd.symbol] = cmd.text

            elif cmd_class_name == "Ingredient":
                if debug:
                    ic(cmd.symbol, cmd.text)

                clos_obj.ingredients[cmd.symbol] = cmd.text

            elif cmd_class_name == "Ratio":
                if debug:
                    ic(cmd.name, [ (elem.symbol, elem.components) for elem in cmd.elements ])

                    for elem in cmd.elements:
                        if elem.symbol not in clos_obj.ingredients:
                            print(f"RATIO component: {elem.symbol} not found")

            elif cmd_class_name == "Add":
                measure: Measure = Measure(
                    amount = cmd.measure.amount,
                    units = cmd.measure.units,
                )

                if debug:
                    ic(cmd.symbol, measure, cmd.text)

                if cmd.symbol not in clos_obj.ingredients:
                    print(f"INGREDIENT: {cmd.symbol} not found")

                clos_obj.focus_op(
                    cmd,
                    OpAdd(
                        symbol = cmd.symbol,
                        measure = measure,
                        text = cmd.text,
                    ),
                )

            elif cmd_class_name == "Use":
                if debug:
                    ic(cmd.symbol, cmd.name)

                clos_obj.ingredients[cmd.symbol] = cmd.name

                clos_obj.focus_op(
                    cmd,
                    OpUse(
                        symbol = cmd.symbol,
                        name = cmd.name,
                    ),
                )

            elif cmd_class_name == "Action":
                duration: Duration = Duration(
                    amount = cmd.duration.amount,
                    units = cmd.duration.units,
                )

                if debug:
                    ic(cmd.symbol, cmd.modifier, cmd.until, duration)

                if cmd.symbol not in clos_obj.tools:
                    print(f"TOOL: {cmd.symbol} not found")

                clos_obj.focus_op(
                    cmd,
                    OpAction(
                        symbol = cmd.symbol,
                        modifier = cmd.modifier,
                        until = cmd.until,
                        duration = duration,
                    ),
                )

            elif cmd_class_name == "Note":
                if debug:
                    ic(cmd.text)

                clos_obj.notes.append(cmd.text)

        return clos_obj


    def interpret (
        self,
        program: typing.Any,
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
