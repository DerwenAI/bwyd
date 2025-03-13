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

from .objects import Dependency, DependencyDict, \
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

            if step_class_name == "Ratio":
                if debug:
                    ic(step_class_name, step.name, [ (part.symbol, part.components) for part in step.parts ])

                    for part in step.parts:
                        if len(part.components) < 1 and part.symbol not in closure_obj.ingredients:
                            print(f"RATIO part: {part.symbol} not found")

            elif step_class_name == "Note":
                if debug:
                    ic(step_class_name, step.text)

                closure_obj.notes.append(step.text)

            elif step_class_name == "Container":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                closure_obj.containers[step.symbol] = Dependency(
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Tool":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                closure_obj.tools[step.symbol] = Dependency(
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Use":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                op: OpUse = OpUse(
                    symbol = step.symbol,
                    text = step.text,
                )

                closure_obj.ingredients[step.symbol] = op

                closure_obj.focus_op(
                    step,
                    op,
                )

            elif step_class_name == "Ingredient":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                closure_obj.ingredients[step.symbol] = Dependency(
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Focus":
                if debug:
                    ic(step_class_name, step.symbol)

                if step.symbol not in closure_obj.containers:
                    print(f"CHILL CONTAINER: {step.symbol} not found")

                closure_obj.active_focus = Focus(
                    container = closure_obj.containers[step.symbol],
                )

                closure_obj.foci.append(closure_obj.active_focus)

            elif step_class_name == "Add":
                measure: Measure = Measure(
                    amount = step.measure.amount,
                    units = step.measure.units,
                )

                if debug:
                    ic(step_class_name, step.symbol, measure, step.text)

                if step.symbol not in closure_obj.ingredients:
                    print(f"INGREDIENT: {step.symbol} not found")

                closure_obj.focus_op(
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
                    ic(step_class_name, step.symbol, step.modifier, step.until, duration)

                equipment: typing.Optional[ typing.Any ] = None

                if step.symbol in closure_obj.tools:
                    equipment = closure_obj.tools[step.symbol]
                elif step.symbol in closure_obj.containers:
                    equipment = closure_obj.containers[step.symbol]
                else:
                    print(f"ACTION OBJECT: {step.symbol} not found")

                closure_obj.focus_op(
                    step,
                    OpAction(
                        tool = equipment,
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

                if step.symbol not in closure_obj.containers:
                    print(f"BAKE CONTAINER: {step.symbol} not found")

                closure_obj.focus_op(
                    step,
                    OpBake(
                        mode = step_class_name,
                        container = closure_obj.containers[step.symbol],
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

                if step.symbol not in closure_obj.containers:
                    print(f"CONTAINER: {step.symbol} not found")

                closure_obj.focus_op(
                    step,
                    OpChill(
                        container = closure_obj.containers[step.symbol],
                        modifier = step.modifier,
                        until = step.until,
                        duration = duration,
                    ),
                )

        return closure_obj


    @classmethod
    def validate_url (
        cls,
        url: str,
        ) -> str:
        """
Parse one URL.
        """
        try:
            result: ParseResult = urlparse(url)

            if result.scheme not in [ "http", "https" ]:
                raise Exception(f"badly formatted URL: {url}")

            return url
        except Exception as ex:
            print(ex)


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
            self.cites.append(self.validate_url(cite.url))

        # parse each `POST`
        for post in module.posts:
            self.posts.append(self.validate_url(post.url))

        # parse each `CLOSURE`
        for closure in module.closures:
            self.closures[closure.name] = self.interpret_closure(
                closure,
                debug = debug,
            )


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
