#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
from urllib.parse import ParseResult, urlparse
import json
import pathlib
import typing

from icecream import ic  # pylint: disable=E0401
import textx  # pylint: disable=E0401
import yattag

from .error import BwydParserError

from .objects import Dependency, DependencyDict, \
    Measure, Duration, Temperature, \
    OpHeader, OpAdd, OpUse, OpAction, OpBake, OpChill, \
    Focus, Closure

from .resources import _CONVERT_PATH


######################################################################
## module definitions

class Module:
    """
One parsed module.
    """
    UNIT_CONVERT: dict = json.load(open(_CONVERT_PATH, "r", encoding = "utf-8"))

    def __init__ (
        self,
        parse_tree: typing.Any,
        ) -> None:
        """
Constructor.
        """
        self.parse_tree: typing.Any = parse_tree
        self.title: str = ""
        self.text: str = ""
        self.cites: typing.List[ str ] = []
        self.posts: typing.List[ str ] = []
        self.closures: typing.Dict[ str, Closure ] = OrderedDict()


    def get_model (
        self,
        ) -> typing.Dict[ str, list ]:
        """
Return a list of JSON-friendly dictionary representations,
one for each parsed Closure.
        """
        closure_list: typing.List[ dict ] = [
            {
                "title": name,
                "yields": closure.yields.to_json(),
                "text": closure.note,
                "requires": closure.get_requires(),
                "foci": [ focus.to_json() for focus in closure.foci ],
            }
            for name, closure in self.closures.items()
        ]

        return {
            "title": self.title,
            "text": self.text,
            "duration": self.total_duration(),
            "serves": closure_list[-1]["yields"]["amount"],
            "image": self.posts[0],
            "sources": self.cites,
            "gallery": self.posts,
            "license": {
                "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
                "image": "https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png",
                "text": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License"
            },
            "closures": closure_list,
        }


    def to_json (
        self,
        ) -> typing.Dict[ str, list ]:
        """
Return a list of JSON-friendly dictionary representations,
one for each parsed Closure.
        """
        closure_list: typing.List[ dict ] = [
            {
                "export": closure.export,
                "note": closure.note,
                "name": name,
                "yields": closure.yields.to_json(),
                "tools": closure.tools.to_json(),
                "containers": closure.containers.to_json(),
                "ingredients": closure.ingredients.to_json(),
                "foci": [ focus.to_json() for focus in closure.foci ],
            }
            for name, closure in self.closures.items()
        ]

        return {
            "cites": self.cites,
            "posts": self.posts,
            "closures": closure_list,
        }


######################################################################
## validation

    @classmethod
    def _validate_url (
        cls,
        entity: typing.Any,
        ) -> str:
        """
Helper method to parse one URL.
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


######################################################################
## parsing methods

    def _interpret_closure (  # pylint: disable=R0912,R0915
        self,
        closure_parse: typing.Any,
        *,
        debug: bool = False,
        ) -> Closure:
        """
Helper method to interpret one Closure.
        """
        # ensure that "null" metadata values keep their semantics
        export: typing.Optional[ str ] = None
        note: typing.Optional[ str ] = None

        if closure_parse.meta is not None:
            if closure_parse.meta.export is not None and len(closure_parse.meta.export) < 1:
                export = None
            if closure_parse.meta.note is not None and len(closure_parse.meta.note) < 1:
                note = None

        closure: Closure = Closure(
            name = closure_parse.name,
            obj = closure_parse,
            yields = Measure(
                amount = closure_parse.yields.amount,
                units = closure_parse.yields.units,
            ),
            export = export,
            note = note,
        )

        for step in closure_parse.steps:
            if debug:
                #ic(dir(closure_parse))
                ic(step)

            step_class_name: str = step.__class__.__name__

            if step_class_name == "Focus":
                if debug:
                    ic(step_class_name, step.symbol)

                # resolve local reference
                if step.symbol in closure.containers:
                    entity: typing.Any = closure.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"CONTAINER `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure.active_focus = Focus(
                    container = entity,
                )

                closure.foci.append(closure.active_focus)

            elif step_class_name == "Header":
                if debug:
                    ic(step_class_name, step.text)

                closure.focus_op(
                    step,
                    OpHeader(
                        loc = textx.get_location(step),
                        text = step.text,
                    )
                )

            if step_class_name == "Container":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                # forward reference, to be resolved during this parsing pass
                closure.containers[step.symbol] = Dependency(
                    loc = textx.get_location(step),
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Tool":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                # forward reference, to be resolved during this parsing pass
                closure.tools[step.symbol] = Dependency(
                    loc = textx.get_location(step),
                    symbol = step.symbol,
                    text = step.text,
                )

            elif step_class_name == "Ingredient":
                if debug:
                    ic(step_class_name, step.symbol, step.text)

                # forward reference, to be resolved during this parsing pass
                closure.ingredients[step.symbol] = Dependency(
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

                closure.ingredients[step.symbol] = op

                closure.focus_op(
                    step,
                    op,
                )

            elif step_class_name == "Add":
                measure: Measure = Measure(
                    amount = step.measure.amount,
                    units = step.measure.units,
                )

                if debug:
                    ic(step_class_name, step.symbol, measure, step.text)

                # resolve local reference
                if step.symbol in closure.ingredients:
                    entity: typing.Any = closure.ingredients[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"INGREDIENT `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure.focus_op(
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

                if step.symbol in closure.tools:
                    entity = closure.tools[step.symbol]
                    entity.ref_count += 1
                elif step.symbol in closure.containers:
                    entity = closure.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"ACTION OBJECT `{step.symbol}` used but not defined {loc}",
                        symbol = symbol,
                    )

                closure.focus_op(
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
                if step.symbol in closure.containers:
                    entity: typing.Any = closure.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"BAKE CONTAINER `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure.focus_op(
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
                if step.symbol in closure.containers:
                    entity: typing.Any = closure.containers[step.symbol]
                    entity.ref_count += 1
                else:
                    loc: dict = textx.get_location(step)

                    raise BwydParserError(
                        f"CHILL CONTAINER `{step.symbol}` used but not defined {loc}",
                        symbol = step.symbol,
                    )

                closure.focus_op(
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
                            if part.symbol in closure.ingredients:
                                entity: typing.Any = closure.ingredients[part.symbol]
                                entity.ref_count += 1
                            else:
                                loc: dict = textx.get_location(part)

                                raise BwydParserError(
                                    f"RATIO part `{part.symbol}` used but not defined {loc}",
                                    symbol = part.symbol,
                                )

        return closure


    def interpret (
        self,
        *,
        debug: bool = False,
        ) -> None:
        """
Interpret one Bwyd module.
        """
        # parse the metadata
        self.title = self.parse_tree.meta.title
        self.text = self.parse_tree.meta.text

        for cite in self.parse_tree.meta.cites:
            self.cites.append(self._validate_url(cite))

        for post in self.parse_tree.meta.posts:
            self.posts.append(self._validate_url(post))

        # parse each `CLOSURE`
        for closure_parse in self.parse_tree.closures:
            self.closures[closure_parse.name] = self._interpret_closure(
                closure_parse,
                debug = debug,
            )

        # validate the resulting parsed module
        self.validate()


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


    def total_yield (
        self,
        ) -> str:
        """
Tally the end yield of one Bwyd module.
        """
        for name, closure in self.closures.items():
            if closure.export is not None:
                return closure.yields.to_html()


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
        export: str = ""

        for name, closure in self.closures.items():
            if closure.export is not None:
                export = closure.export

        doc, tag, text = yattag.Doc().tagtext()
        doc.asis("<!DOCTYPE html>")

        with tag("html", lang = lang):
            with tag("head"):
                doc.stag("meta", charset = charset)
                doc.stag("meta", name = "viewport", content = viewport)
                doc.stag("link", rel = "stylesheet", href = stylesheet)
                doc.stag("link", rel = "icon", href = "bwyd/resources/bwyd.svg")

                with tag("export"):
                    text(export)

            with tag("body"):
                with tag("h1"):
                    text(export)

                # metadata
                with tag("p"):
                    text("time: ")

                    with tag("strong"):
                        with tag("time"):
                            text(self.total_duration())

                    doc.stag("br")
                    text("yields: ")

                    with tag("strong"):
                        text(self.total_yield())

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
