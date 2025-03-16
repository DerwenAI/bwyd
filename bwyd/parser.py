#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from urllib.parse import ParseResult, urlparse
import json
import pathlib
import typing

from icecream import ic  # pylint: disable=E0401
import textx  # pylint: disable=E0401
import yattag

from .objects import BwydParserError, \
    Dependency, DependencyDict, \
    Measure, Duration, Temperature, \
    OpAdd, OpUse, OpAction, OpBake, OpChill, \
    Focus, Closure

from .resources import _CONVERT_PATH, _GRAMMAR_PATH


######################################################################
## parser/interpreter definitions

class Bwyd:
    """
Bwyd DSL parser/interpreter.
    """
    META_MODEL: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        _GRAMMAR_PATH,
        debug = False, # True
    )

    UNIT_CONVERT: dict = json.load(open(_CONVERT_PATH, "r", encoding = "utf-8"))


    def __init__ (
        self,
        ) -> None:
        """
Constructor.
        """
        self.cites: typing.List[ str ] = []
        self.posts: typing.List[ str ] = []
        self.closures: typing.Dict[ str, Closure ] = {}


    def to_json (
        self,
        ) -> typing.Dict[ str, list ]:
        """
Return a list of JSON-friendly dictionary representations,
one for each parsed Closure.
        """
        closure_list: typing.List[ dict ] = [
            {
                "title": closure_obj.title,
                "name": name,
                "yields": closure_obj.yields.to_json(),
                "notes": closure_obj.notes,
                "tools": closure_obj.tools.to_json(),
                "containers": closure_obj.containers.to_json(),
                "ingredients": closure_obj.ingredients.to_json(),
                "foci": [ focus.to_json() for focus in closure_obj.foci ],
            }
            for name, closure_obj in self.closures.items()
        ]

        return {
            "cites": self.cites,
            "posts": self.posts,
            "closures": closure_list,
        }


######################################################################
## parse and interpret one module

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
        # ensure that "null" titles keep their anonymous semantics
        title: typing.Optional[ str ] = closure.title

        if title is not None and len(title) < 1:
            title = None

        closure_obj: Closure = Closure(
            name = closure.name,
            obj = closure,
            yields = Measure(
                amount = closure.yields.amount,
                units = closure.yields.units,
            ),
            title = title,
        )

        for step in closure.steps:
            if debug:
                #ic(dir(closure))
                ic(step)

            step_class_name: str = step.__class__.__name__

            if step_class_name == "Note":
                if debug:
                    ic(step_class_name, step.text)

                closure_obj.notes.append(step.text)

            elif step_class_name == "Container":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                # forward reference, to be resolved during this parsing pass
                closure_obj.containers[step.symbol] = Dependency(
                    loc = textx.get_location(step),
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Tool":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                # forward reference, to be resolved during this parsing pass
                closure_obj.tools[step.symbol] = Dependency(
                    loc = textx.get_location(step),
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Ingredient":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                # forward reference, to be resolved during this parsing pass
                closure_obj.ingredients[step.symbol] = Dependency(
                    loc = textx.get_location(step),
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Use":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                # forward reference, to be resolved on a subsequent pass
                op: OpUse = OpUse(
                    loc = textx.get_location(step),
                    symbol = step.symbol,
                    text = step.text,
                )

                closure_obj.ingredients[step.symbol] = op

                closure_obj.focus_op(
                    step,
                    op,
                )

            elif step_class_name == "Focus":
                if debug:
                    ic(step_class_name, step.symbol)

                # resolve local reference
                if step.symbol in closure_obj.containers:
                    entity: typing.Any = closure_obj.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"CONTAINER `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure_obj.active_focus = Focus(
                    container = entity,
                )

                closure_obj.foci.append(closure_obj.active_focus)

            elif step_class_name == "Add":
                measure: Measure = Measure(
                    amount = step.measure.amount,
                    units = step.measure.units,
                )

                if debug:
                    ic(step_class_name, step.symbol, measure, step.text)

                # resolve local reference
                if step.symbol in closure_obj.ingredients:
                    entity: typing.Any = closure_obj.ingredients[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"INGREDIENT `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure_obj.focus_op(
                    step,
                    OpAdd(
                        loc = textx.get_location(step),
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
                    ic(step_class_name, step.symbol, step.modifier, step.until, duration)

                # resolve local reference
                entity: typing.Optional[ typing.Any ] = None

                if step.symbol in closure_obj.tools:
                    entity = closure_obj.tools[step.symbol]
                    entity.ref_count += 1
                elif step.symbol in closure_obj.containers:
                    entity = closure_obj.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"ACTION OBJECT `{step.symbol}` used but not defined {loc}",
                        symbol = symbol,
                    )

                closure_obj.focus_op(
                    step,
                    OpAction(
                        loc = textx.get_location(step),
                        tool = entity,
                        modifier = step.modifier,
                        until = step.until,
                        duration = duration,
                    ),
                )

            elif step_class_name == "Bake":
                temperature = Temperature(
                    amount = step.temperature.amount,
                    units = step.temperature.units,
                )

                duration = Duration(
                    amount = step.duration.amount,
                    units = step.duration.units,
                )

                if debug:
                    ic(step_class_name, step.symbol, step.modifier, step.until, temperature, duration)

                # resolve local reference
                if step.symbol in closure_obj.containers:
                    entity: typing.Any = closure_obj.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"BAKE CONTAINER `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure_obj.focus_op(
                    step,
                    OpBake(
                        loc = textx.get_location(step),
                        mode = step_class_name,
                        container = entity,
                        modifier = step.modifier,
                        until = step.until,
                        duration = duration,
                        temperature = temperature,
                    ),
                )

            elif step_class_name == "Chill":
                duration = Duration(
                    amount = step.duration.amount,
                    units = step.duration.units,
                )

                if debug:
                    ic(step_class_name, step.symbol, step.modifier, step.until, duration)

                # resolve local reference
                if step.symbol in closure_obj.containers:
                    entity: typing.Any = closure_obj.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"CHILL CONTAINER `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure_obj.focus_op(
                    step,
                    OpChill(
                        loc = textx.get_location(step),
                        container = entity,
                        modifier = step.modifier,
                        until = step.until,
                        duration = duration,
                    ),
                )

            elif step_class_name == "Ratio":
                if debug:
                    ic(step_class_name, step.name, [ (part.symbol, part.components) for part in step.parts ])

                    for part in step.parts:
                        if len(part.components) < 1:
                            # resolve local reference
                            if part.symbol in closure_obj.ingredients:
                                entity: typing.Any = closure_obj.ingredients[part.symbol]
                                entity.ref_count += 1
                            else:
                                loc: dict = textx.get_location(part)

                                raise BwydParserError(
                                    f"RATIO part `{part.symbol}` used but not defined {loc}",
                                    symbol = part.symbol,
                                )

        return closure_obj


    def interpret (
        self,
        module: typing.Any,
        *,
        debug: bool = False,
        ) -> None:
        """
Interpret one Bwyd module.
        """
        # parse each `CITE`
        for cite in module.cites:
            self.cites.append(self.validate_url(cite))

        # parse each `POST`
        for post in module.posts:
            self.posts.append(self.validate_url(post))

        # parse each `CLOSURE`
        for closure in module.closures:
            self.closures[closure.name] = self.interpret_closure(
                closure,
                debug = debug,
            )


######################################################################
## aggregate measures

    def total_duration (
        self,
        ) -> str:
        """
Tally the total duration of one Bwyd module.
        """
        total_sec: int = sum([
            op.get_duration().normalize()
            for closure in self.closures.values()
            for focus in closure.foci
            for op in focus.ops
        ])

        return Duration(total_sec, "sec").humanize()


######################################################################
## HTML representation

    def to_html (
        self,
        *,
        lang: str = "en",
        charset: str = "UTF-8",
        viewport: str = "width=device-width, initial-scale=1.0",
        stylesheet: str = "style.css",
        indent: bool = False,
        ) -> str:
        """
Generate an HTML representation.
        """
        title: str = ""

        for name, closure in self.closures.items():
            if closure.title is not None:
                title = closure.title

        doc, tag, text = yattag.Doc().tagtext()
        doc.asis("<!DOCTYPE html>")

        with tag("html", lang = lang):
            with tag("head"):
                doc.stag("meta", charset = charset)
                doc.stag("meta", name = "viewport", content = viewport)
                doc.stag("link", rel = "stylesheet", href = stylesheet)
                doc.stag("link", rel = "icon", href = "bwyd/resources/bwyd.svg")

                with tag("title"):
                    text(title)

            with tag("body"):
                with tag("h1"):
                    text(title)

                # metadata
                with tag("p"):
                    text("total time: ")

                    with tag("strong"):
                        with tag("time"):
                            text(self.total_duration())

                # cites
                if len(self.cites) > 0:
                        with tag("p"):
                            text("sources")

                            with tag("ul"):
                                for cite in self.cites:
                                    with tag("li"):
                                        with tag("a", href = cite, target = "_blank"):
                                            text(cite)

                # posts
                if len(self.posts) > 0:
                    with tag("p"):
                        text("gallery")

                        with tag("ul"):
                            for post in self.posts:
                                with tag("li"):
                                    with tag("a", href = post, target = "_blank"):
                                        text(post)

                with tag("h2"):
                    text("directions:")

                for _, closure in self.closures.items():
                    closure.to_html(doc, tag, text, self.UNIT_CONVERT)

        if indent:
            return yattag.indent(doc.getvalue())

        return doc.getvalue()



######################################################################
## validation

    @classmethod
    def validate_url (
        cls,
        entity: typing.Any,
        ) -> str:
        """
Parse one URL.
        """
        try:
            loc: dict = textx.get_location(entity)
            url: str = entity.url
            result: ParseResult = urlparse(url)

            if result.scheme not in [ "http", "https" ]:
                raise BwydParserError(
                    f"badly formatted URL `{url}` referenced at {loc}",
                    symbol = url,
                )

            return url
        except Exception as ex:
            print(ex)


    def validate (
        self,
        module: typing.Any,
        ) -> None:
        """
Validate the forward references for one Bwyd module.
        """
        local_names: typing.Set[ str ] = set(self.closures.keys())

        for closure in self.closures.values():
            # check for zero reference counts
            for name, entity in closure.containers.items():
                if entity.ref_count < 1:
                    print(f"Container defined but not used: {name}")
                    print(entity.loc)

            for name, entity in closure.tools.items():
                if entity.ref_count < 1:
                    print(f"Tool defined but not used: {name}")
                    print(entity.loc)

            for name, entity in closure.ingredients.items():
                if entity.ref_count < 1:
                    print(f"Ingredient defined but not used: {name}")
                    print(entity.loc)

            # check for references outside this module
            for symbol, op in closure.ingredients.items():
                if isinstance(op, OpUse) and symbol not in local_names:
                    raise BwydParserError(
                        f"CLOSURE `{symbol}` used but not defined {op.loc}",
                        symbol = symbol,
                    )
