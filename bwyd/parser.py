#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from urllib.parse import ParseResult, urlparse
import pathlib
import typing

from icecream import ic  # pylint: disable=E0401
import textx  # pylint: disable=E0401
import yattag

from .objects import Duration, Measure, Temperature, \
    OpAction, OpAdd, OpBake, OpChill, OpUse, \
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
        clos_list: typing.List[ dict ] = [
            {
                "title": clos_obj.title,
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

        return {
            "cites": self.cites,
            "posts": self.posts,
            "closures": clos_list,
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

        clos_obj: Closure = Closure(
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
                        if len(part.components) < 1 and part.symbol not in clos_obj.ingredients:
                            print(f"RATIO part: {part.symbol} not found")

            elif step_class_name == "Note":
                if debug:
                    ic(step_class_name, step.text)

                clos_obj.notes.append(step.text)

            elif step_class_name == "Container":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                clos_obj.containers[step.symbol] = step.text

            elif step_class_name == "Tool":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                clos_obj.tools[step.symbol] = step.text

            elif step_class_name == "Use":
                if debug:
                    ic(step_class_name, step.symbol, step.name)

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
                    ic(step_class_name, step.symbol, step.text)

                clos_obj.ingredients[step.symbol] = step.text

            elif step_class_name == "Focus":
                if debug:
                    ic(step_class_name, step.symbol)

                if step.symbol not in clos_obj.containers:
                    print(f"CHILL CONTAINER: {step.symbol} not found")

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
                    ic(step_class_name, step.symbol, measure, step.text)

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
                    ic(step_class_name, step.symbol, step.modifier, step.until, duration)

                if step.symbol not in clos_obj.tools and step.symbol not in clos_obj.containers:
                    print(f"ACTION OBJECT: {step.symbol} not found")

                clos_obj.focus_op(
                    step,
                    OpAction(
                        tool = step.symbol,
                        modifier = step.modifier,
                        until = step.until,
                        duration = duration,
                    ),
                )

            elif step_class_name == "Bake":
                temperature = Temperature(
                    degrees = step.temperature.degrees,
                    units = step.temperature.units,
                )

                duration = Duration(
                    amount = step.duration.amount,
                    units = step.duration.units,
                )

                if debug:
                    ic(step_class_name, step.symbol, step.modifier, step.until, temperature, duration)

                if step.symbol not in clos_obj.containers:
                    print(f"BAKE CONTAINER: {step.symbol} not found")

                clos_obj.focus_op(
                    step,
                    OpBake(
                        mode = step_class_name,
                        container = step.symbol,
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

                if step.symbol not in clos_obj.containers:
                    print(f"CONTAINER: {step.symbol} not found")

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
Process interpreter for one Bwyd module.
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
Generate an HTML representation
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

                # cites
                if len(self.cites) > 0:
                    with tag("h2"):
                        text("Sources:")

                    with tag("ul"):
                        for cite in self.cites:
                            with tag("li"):
                                with tag("a", href = cite, target = "_blank"):
                                    text(cite)

                # posts
                if len(self.posts) > 0:
                    with tag("h2"):
                        text("Gallery:")

                    with tag("ul"):
                        for post in self.posts:
                            with tag("li"):
                                with tag("a", href = post, target = "_blank"):
                                    text(post)

                with tag("h2"):
                    text("Directions:")

                for _, closure in self.closures.items():
                    closure.to_html(doc, tag, text)

        if indent:
            return yattag.indent(doc.getvalue())

        return doc.getvalue()
