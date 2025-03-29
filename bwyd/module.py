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
import jinja2
import textx  # pylint: disable=E0401

from .error import BwydParserError

from .objects import Dependency, DependencyDict, \
    Measure, Duration, Temperature, \
    OpsTypes, OpAdd, OpAction, OpBake, OpChill, \
    Activity, Focus, Closure

from .resources import _CONVERT_PATH, _JINJA_TEMPLATE


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
                "yields": closure.yields.humanize(),
                "text": closure.text,
                "requires": closure.get_dependencies(),
                "foci": [ focus.get_model(self.UNIT_CONVERT) for focus in closure.foci ],
            }
            for name, closure in self.closures.items()
        ]

        ## TODO: make the image URL embeddable in an <iframe/>
        img_embed_url: str = self.posts[0] + "embed"

        ## TODO: structure the license spec in the language

        return {
            "title": self.title,
            "text": self.text,
            "duration": self.total_duration(),
            "serves": closure_list[-1]["yields"],
            "image": img_embed_url,
            "sources": self.cites,
            "gallery": self.posts,
            "license": {
                "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
                "image": "https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png",
                "text": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License"
            },
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
            for symbol, entity in closure.ingredients.items():
                if entity.external and symbol not in local_names:
                    raise BwydParserError(
                        f"CLOSURE `{symbol}` used but not defined {entity.loc}",
                        symbol = symbol,
                    )


######################################################################
## parsing methods

    def _interpret_dependency (
        self,
        closure: Closure,
        depend_parse: typing.Any,
        *,
        debug: bool = False,
        ) -> None:
        """
Interpret and resolve each dependency: container, tool, ingredient, use.
        """
        depend_class_name: str = depend_parse.__class__.__name__

        if debug:
            #ic(dir(depend_parse))
            ic(depend_parse)
            ic(depend_class_name, depend_parse.symbol, depend_parse.text)

        if depend_class_name == "Container":
            # forward reference, to be resolved during this parsing pass
            closure.containers[depend_parse.symbol] = Dependency(
                loc = textx.get_location(depend_parse),
                symbol = depend_parse.symbol,
                text = depend_parse.text,
            )

        elif depend_class_name == "Tool":
            # forward reference, to be resolved during this parsing pass
            closure.tools[depend_parse.symbol] = Dependency(
                loc = textx.get_location(depend_parse),
                symbol = depend_parse.symbol,
                text = depend_parse.text,
            )

        elif depend_class_name == "Ingredient":
            # forward reference, to be resolved during this parsing pass
            closure.ingredients[depend_parse.symbol] = Dependency(
                loc = textx.get_location(depend_parse),
                symbol = depend_parse.symbol,
                text = depend_parse.text,
            )

        elif depend_class_name == "Use":
            # external forward reference, to be resolved on a subsequent pass
            closure.ingredients[depend_parse.symbol] = Dependency(
                loc = textx.get_location(depend_parse),
                symbol = depend_parse.symbol,
                text = depend_parse.text,
                external = True,
            )


    def _interpret_op (
        self,
        closure: Closure,
        op_parse: typing.Any,
        *,
        debug: bool = False,
        ) -> typing.Optional[ OpsTypes ]:
        """
Interpret the steps within an activity.
        """
        op_class_name: str = op_parse.__class__.__name__

        if debug:
            ic(op_parse, op_parse.symbol)

        if op_class_name == "Add":
            measure: Measure = Measure(
                amount = op_parse.measure.amount,
                units = op_parse.measure.units,
            )

            if debug:
                ic(op_class_name, op_parse.symbol, measure, op_parse.text)

            # resolve local reference
            if op_parse.symbol in closure.ingredients:
                entity: typing.Any = closure.ingredients[op_parse.symbol]
                entity.ref_count += 1
            else:
                loc: dict = textx.get_location(op_parse)

                raise BwydParserError(
                    f"INGREDIENT `{op_parse.symbol}` used but not defined {loc}",
                    symbol = op_parse.symbol,
                )

            return OpAdd(
                loc = textx.get_location(op_parse),
                symbol = op_parse.symbol,
                measure = measure,
                text = op_parse.text,
            )

        elif op_class_name == "Action":
            duration: Duration = Duration(
                amount = op_parse.duration.amount,
                units = op_parse.duration.units,
            )

            if debug:
                ic(op_class_name, op_parse.symbol, op_parse.modifier, op_parse.until, duration)

            # resolve local reference
            entity: typing.Optional[ typing.Any ] = None

            if op_parse.symbol in closure.tools:
                entity = closure.tools[op_parse.symbol]
                entity.ref_count += 1
            elif op_parse.symbol in closure.containers:
                entity = closure.containers[op_parse.symbol]
                entity.ref_count += 1
            else:
                loc: dict = textx.get_location(op_parse)

                raise BwydParserError(
                    f"ACTION OBJECT `{op_parse.symbol}` used but not defined {loc}",
                    symbol = symbol,
                )

            return OpAction(
                loc = textx.get_location(op_parse),
                tool = entity,
                modifier = op_parse.modifier,
                until = op_parse.until,
                duration = duration,
            )

        elif op_class_name == "Bake":
            temperature = Temperature(
                amount = op_parse.temperature.amount,
                units = op_parse.temperature.units,
            )

            duration = Duration(
                amount = op_parse.duration.amount,
                units = op_parse.duration.units,
            )

            if debug:
                ic(op_class_name, op_parse.symbol, op_parse.modifier, op_parse.until, temperature, duration)

            # resolve local reference
            if op_parse.symbol in closure.containers:
                entity: typing.Any = closure.containers[op_parse.symbol]
                entity.ref_count += 1
            else:
                loc: dict = textx.get_location(op_parse)

                raise BwydParserError(
                    f"BAKE CONTAINER `{op_parse.symbol}` used but not defined {loc}",
                    symbol = op_parse.symbol,
                )

            return OpBake(
                loc = textx.get_location(op_parse),
                mode = op_class_name,
                container = entity,
                modifier = op_parse.modifier,
                until = op_parse.until,
                duration = duration,
                temperature = temperature,
            )

        elif op_class_name == "Chill":
            duration = Duration(
                amount = op_parse.duration.amount,
                units = op_parse.duration.units,
            )

            if debug:
                ic(op_class_name, op_parse.symbol, op_parse.modifier, op_parse.until, duration)

            # resolve local reference
            if op_parse.symbol in closure.containers:
                entity: typing.Any = closure.containers[op_parse.symbol]
                entity.ref_count += 1
            else:
                loc: dict = textx.get_location(op_parse)

                raise BwydParserError(
                    f"CHILL CONTAINER `{op_parse.symbol}` used but not defined {loc}",
                    symbol = op_parse.symbol,
                )

            return OpChill(
                loc = textx.get_location(op_parse),
                container = entity,
                modifier = op_parse.modifier,
                until = op_parse.until,
                duration = duration,
            )

        return None


    def _interpret_focus (
        self,
        closure: Closure,
        focus_parse: typing.Any,
        *,
        debug: bool = False,
        ) -> None:
        """
Interpret the activities within a focus.
        """
        if debug:
            ic(focus_parse, focus_parse.symbol)

        # resolve local reference
        if focus_parse.symbol in closure.containers:
            entity: typing.Any = closure.containers[focus_parse.symbol]
            entity.ref_count += 1
        else:
            loc: dict = textx.get_location(focus_parse)

            raise BwydParserError(
                f"CONTAINER `{focus_parse.symbol}` used but not defined {loc}",
                symbol = focus_parse.symbol,
            )

        focus = Focus(
            container = entity,
        )

        closure.foci.append(focus)

        for activity in focus_parse.activities:
            if debug:
                ic(activity, activity.text)

            act: Activity = Activity(
                text = activity.text,
            )

            focus.activities.append(act)

            for op_parse in activity.ops:
                op_obj: OpsTypes = self._interpret_op(
                    closure,
                    op_parse,
                    debug = debug,
                )

                act.ops.append(op_obj)
 

    def _interpret_ratio (
        self,
        closure: Closure,
        ratio_parse: typing.Any,
        *,
        debug: bool = False,
        ) -> None:
        """
Interpret the components within a ratio.
        """
        if debug:
            ic(ratio_parse.name, [ (part.symbol, part.components) for part in ratio_parse.parts ])

        for part in ratio_parse.parts:
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

            ## TODO: store representation of this ratio


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
        text: str = ""

        if closure_parse.meta is not None:
            if closure_parse.meta.export is not None and len(closure_parse.meta.export) > 0:
                export = closure_parse.meta.export

            if closure_parse.meta.text is not None and len(closure_parse.meta.text) > 0:
                text = closure_parse.meta.text            

        closure: Closure = Closure(
            name = closure_parse.symbol,
            obj = closure_parse,
            yields = Measure(
                amount = closure_parse.yields.amount,
                units = closure_parse.yields.units,
            ),
            export = export,
            text = text,
        )

        # resolve each dependency
        for depend_parse in closure_parse.depend:
            self._interpret_dependency(
                closure,
                depend_parse,
                debug = debug,
            )

        # interpret each focus
        for focus_parse in closure_parse.foci:
            self._interpret_focus(
                closure,
                focus_parse,
                debug = debug,
            )

        # interpret the ratio specification, if any
        if closure_parse.ratio is not None:
            self._interpret_ratio(
                closure,
                closure_parse.ratio,
                debug = debug,
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
            self.closures[closure_parse.symbol] = self._interpret_closure(
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
Accessor for the total duration of one Bwyd module.
        """
        total_sec: int = sum([
            op.get_duration().normalize()
            for closure in self.closures.values()
            for focus in closure.foci
            for activity in focus.activities
            for op in activity.ops
        ])

        return Duration(total_sec, "sec").humanize()


    def total_yield (
        self,
        ) -> str:
        """
Accessor for the total yield of one Bwyd module.
        """
        return list(self.closures.values())[-1]["yields"]


######################################################################
## Jinja2 template rendering

    def render_template (
        self,
        *,
        template: jinja2.Template = _JINJA_TEMPLATE,
        ) -> str:
        """
Load a Jinja2 template and render the data model as HTML.
        """
        return template.render(
            module = self.get_model()
        )
