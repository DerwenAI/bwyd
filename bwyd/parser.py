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
    OpAction, OpAdd, OpChill, OpUse, \
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

        for step in closure.steps:
            if debug:
                #ic(dir(closure))
                ic(step)

            step_class_name: str = step.__class__.__name__

            if step_class_name == "Ratio":
                if debug:
                    ic(step.name, [ (elem.symbol, elem.components) for elem in step.elements ])

                    for elem in step.elements:
                        if elem.symbol not in clos_obj.ingredients:
                            print(f"RATIO component: {elem.symbol} not found")

            elif step_class_name == "Note":
                if debug:
                    ic(step.text)

                clos_obj.notes.append(step.text)

            elif step_class_name == "Container":
                if debug:
                    ic(step.symbol, step.text)

                clos_obj.containers[step.symbol] = step.text

            elif step_class_name == "Tool":
                if debug:
                    ic(step.symbol, step.text)

                clos_obj.tools[step.symbol] = step.text

            elif step_class_name == "Use":
                if debug:
                    ic(step.symbol, step.name)

                clos_obj.ingredients[step.symbol] = step.name

                clos_obj.focus_op(
                    step,
                    OpUse(
                        symbol = step.symbol,
                        name = step.name,
                    ),
                )

            elif step_class_name == "Ingredient":
                if debug:
                    ic(step.symbol, step.text)

                clos_obj.ingredients[step.symbol] = step.text

            elif step_class_name == "Focus":
                if debug:
                    ic(step.symbol)

                if step.symbol not in clos_obj.containers:
                    print(f"CONTAINER: {step.symbol} not found")

                clos_obj.active_focus = Focus(
                    container = step.symbol,
                )

                clos_obj.foci.append(clos_obj.active_focus)

            elif step_class_name == "Add":
                measure: Measure = Measure(
                    amount = step.measure.amount,
                    units = step.measure.units,
                )

                if debug:
                    ic(step.symbol, measure, step.text)

                if step.symbol not in clos_obj.ingredients:
                    print(f"INGREDIENT: {step.symbol} not found")

                clos_obj.focus_op(
                    step,
                    OpAdd(
                        symbol = step.symbol,
                        measure = measure,
                        text = step.text,
                    ),
                )

            elif step_class_name == "Action":
                duration: Duration = Duration(
                    amount = step.duration.amount,
                    units = step.duration.units,
                )

                if debug:
                    ic(step.symbol, step.modifier, step.until, duration)

                if step.symbol not in clos_obj.tools:
                    print(f"TOOL: {step.symbol} not found")

                clos_obj.focus_op(
                    step,
                    OpAction(
                        tool = step.symbol,
                        modifier = step.modifier,
                        until = step.until,
                        duration = duration,
                    ),
                )

            elif step_class_name == "Chill":
                duration = Duration(
                    amount = step.duration.amount,
                    units = step.duration.units,
                )

                if debug:
                    ic(step.symbol, step.modifier, step.until, duration)

                if step.symbol not in clos_obj.containers:
                    print(f"TOOL: {step.symbol} not found")

                clos_obj.focus_op(
                    step,
                    OpChill(
                        container = step.symbol,
                        modifier = step.modifier,
                        until = step.until,
                        duration = duration,
                    ),
                )

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
