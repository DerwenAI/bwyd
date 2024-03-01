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

__version__ = "0.1"


######################################################################
## class definitions                                                                                                                        

@dataclass(order=False, frozen=False)
class Measure:  # pylint: disable=R0902
    """
A data class representing one parsed Measure object.
    """
    amount: float
    units: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "amount": self.amount,
            "units": self.units,
        }


@dataclass(order=False, frozen=False)
class Duration:  # pylint: disable=R0902
    """
A data class representing one parsed Duration object.
    """
    amount: float
    units: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "amount": self.amount,
            "units": self.units,
        }


@dataclass(order=False, frozen=False)
class OpAdd:  # pylint: disable=R0902
    """
A data class representing one Add object.
    """
    symbol: str
    measure: Measure
    text: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "op": "add",
            "symbol": self.symbol,
            "measure": self.measure.to_json(),
            "text": self.text,
        }


@dataclass(order=False, frozen=False)
class OpUse:  # pylint: disable=R0902
    """
A data class representing one Use object.
    """
    symbol: str
    name: str

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "op": "use",
            "symbol": self.symbol,
            "name": self.name,
        }


@dataclass(order=False, frozen=False)
class OpAction:  # pylint: disable=R0902
    """
A data class representing one Action object.
    """
    symbol: str
    modifier: str
    until: str
    duration: Duration

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "op": "action",
            "symbol": self.symbol,
            "modifier": self.modifier,
            "until": self.until,
            "duration": self.duration.to_json(),
        }


@dataclass(order=False, frozen=False)
class Focus:  # pylint: disable=R0902
    """
A data class representing a parsed Focus object.
    """
    symbol: str
    ops: typing.List[typing.Union[ OpAdd, OpUse, OpAction ]] = field(default_factory = lambda: [])    

    def to_json (
        self
        ) -> dict:
        """
Serializable representation for JSON.
        """
        return {
            "symbol": self.symbol,
            "ops": [ op.to_json() for op in self.ops ],
        }


@dataclass(order=False, frozen=False)
class Closure:  # pylint: disable=R0902
    """
A data class representing one parsed Closure object.
    """
    name: str
    obj: typing.Any
    yields: Measure
    notes: typing.List[ str ] = field(default_factory = lambda: [])
    tools: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())
    containers: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())
    ingredients: typing.Dict[ str, str ] = field(default_factory = lambda: OrderedDict())
    foci: typing.List[ Focus ] = field(default_factory = lambda: [])
    active_focus: typing.Optional[ Focus ] = None

    def focus_op (
        self,
        cmd,
        op: typing.Union[ OpAdd, OpUse, OpAction ],
        ) -> None:
        """
Append one operation to the active Focus.        
        """
        print(type(cmd))

        if self.active_focus is None:
            print(f"FOCUS: not defined yet for {cmd.symbol}")
        else:
            self.active_focus.ops.append(op)


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


    def to_json (
        self,
        ) -> typing.List[dict]:
        """
Return a list of JSON-friendly dictionary representations, one for
each parsed Closure.
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
            yields = Measure(
                amount = closure.yields.amount,
                units = closure.yields.units,
            ),
        )

        for cmd in closure.commands:
            if debug:
                #ic(dir(closure))
                ic(cmd)

            match cmd.__class__.__name__:
                case "Container":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    clos_obj.containers[cmd.symbol] = cmd.text

                case "Focus":
                    if debug:
                        ic(cmd.symbol)

                    if cmd.symbol not in clos_obj.containers:
                        print(f"CONTAINER: {cmd.symbol} not found")

                    clos_obj.active_focus = Focus(
                        symbol = cmd.symbol,
                    )

                    clos_obj.foci.append(clos_obj.active_focus)

                case "Tool":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    clos_obj.tools[cmd.symbol] = cmd.text

                case "Ingredient":
                    if debug:
                        ic(cmd.symbol, cmd.text)

                    clos_obj.ingredients[cmd.symbol] = cmd.text

                case "Ratio":
                    if debug:
                        ic(cmd.name, [ (elem.symbol, elem.components) for elem in cmd.elements ])

                        for elem in cmd.elements:
                            if elem.symbol not in clos_obj.ingredients:
                                print(f"RATIO component: {elem.symbol} not found")

                case "Add":
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
                        )
                    )

                case "Use":
                    if debug:
                        ic(cmd.symbol, cmd.name)

                    clos_obj.ingredients[cmd.symbol] = cmd.name

                    clos_obj.focus_op(
                        cmd,
                        OpUse(
                            symbol = cmd.symbol,
                            name = cmd.name,
                        )
                    )

                case "Action":
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
                        )
                    )

                case "Note":
                    if debug:
                        ic(cmd.text)

                    clos_obj.notes.append(cmd.text)

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
        bwyd.to_json(),
        indent = 2,
        sort_keys = False,
    ))
