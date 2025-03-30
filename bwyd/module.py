#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import OrderedDict
from urllib.parse import ParseResult, urlparse
import json
import typing

from icecream import ic  # type: ignore  # pylint: disable=E0401
import jinja2
import textx  # type: ignore  # pylint: disable=E0401

from .error import BwydParserError

from .measure import Measure, Duration, Temperature

from .ops import Dependency, \
    OpsTypes, OpAdd, OpAction, OpBake, OpChill

from .resources import _CONVERT_PATH, _JINJA_TEMPLATE

from .structure import Product, \
    Activity, Focus, Closure


######################################################################
## module definitions

class Module:
    """
One parsed module.
    """
    UNIT_CONVERT: dict = json.load(open(_CONVERT_PATH, "r", encoding = "utf-8"))  # pylint: disable=R1732

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


    def get_image (
        self,
        ) -> str:
        """
Make the image URL embeddable in an <iframe/>
        """
        img_url: str = ""

        if len(self.posts) > 0:
            img_url = self.posts[0]

        if "instagram.com" in img_url:
            return img_url + "embed"

        return img_url


    def get_model (
        self,
        ) -> dict:
        """
Return a list of JSON-friendly dictionary representations,
one for each parsed Closure.
        """
        closure_list: typing.List[ dict ] = [
            {
                "title": name,
                "yields": closure.total_yields(intermediaries = True),
                "text": closure.text,
                "requires": closure.get_dependencies(),
                "foci": [ focus.get_model(self.UNIT_CONVERT) for focus in closure.foci ],
            }
            for name, closure in self.closures.items()
        ]

        ## FUCK: structure the license spec in the language

        return {
            "title": self.title,
            "text": self.text,
            "duration": self.total_duration(),
            "serves": self.total_yields(),
            "image": self.get_image(),
            "sources": self.cites,
            "gallery": self.posts,
            "license": {
                "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
                "image": "https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png",  # pylint: disable=C0301
                "text": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License"  # pylint: disable=C0301
            },
            "closures": closure_list,
        }


######################################################################
## validation

    @classmethod
    def _validate_url (  # type: ignore  # pylint: disable=R1710
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

        except Exception as ex:  # pylint: disable=W0718
            print(ex)


    def validate (
        self,
        ) -> None:
        """
Validate the forward references for one Bwyd module.
        """
        local_names: typing.Set[ str ] = {
            product.symbol
            for closure in self.closures.values()
            for product in closure.products
        }

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


    def _interpret_op (  # pylint: disable=R0912
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

        if op_class_name == "Action":
            duration: Duration = Duration(
                amount = op_parse.duration.amount,
                units = op_parse.duration.units,
            )

            if debug:
                ic(op_class_name, op_parse.symbol, op_parse.modifier, op_parse.until, duration)

            # resolve local reference
            entity = None

            if op_parse.symbol in closure.tools:
                entity = closure.tools[op_parse.symbol]
                entity.ref_count += 1
            elif op_parse.symbol in closure.containers:
                entity = closure.containers[op_parse.symbol]
                entity.ref_count += 1
            else:
                loc = textx.get_location(op_parse)

                raise BwydParserError(
                    f"ACTION OBJECT `{op_parse.symbol}` used but not defined {loc}",
                    symbol = op_parse.symbol,
                )

            return OpAction(
                loc = textx.get_location(op_parse),
                tool = entity,
                modifier = op_parse.modifier,
                until = op_parse.until,
                duration = duration,
            )

        if op_class_name == "Bake":
            temperature = Temperature(
                amount = op_parse.temperature.amount,
                units = op_parse.temperature.units,
            )

            duration = Duration(
                amount = op_parse.duration.amount,
                units = op_parse.duration.units,
            )

            if debug:
                ic(op_class_name, op_parse.symbol, op_parse.modifier, op_parse.until, temperature, duration)  # pylint: disable=C0301

            # resolve local reference
            if op_parse.symbol in closure.containers:
                entity = closure.containers[op_parse.symbol]
                entity.ref_count += 1
            else:
                loc = textx.get_location(op_parse)

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

        if op_class_name == "Chill":
            duration = Duration(
                amount = op_parse.duration.amount,
                units = op_parse.duration.units,
            )

            if debug:
                ic(op_class_name, op_parse.symbol, op_parse.modifier, op_parse.until, duration)

            # resolve local reference
            if op_parse.symbol in closure.containers:
                entity = closure.containers[op_parse.symbol]
                entity.ref_count += 1
            else:
                loc = textx.get_location(op_parse)

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
                op_obj: OpsTypes = self._interpret_op(  # type: ignore
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

            ## FUCK: store representation of this ratio


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
        text: str = ""

        if closure_parse.meta is not None:
            if closure_parse.meta.text is not None and len(closure_parse.meta.text) > 0:
                text = closure_parse.meta.text

        closure: Closure = Closure(
            name = closure_parse.name,
            obj = closure_parse,
            text = text,
        )

        # interpret each product
        for prod_parse in closure_parse.prods:
            if debug:
                ic(prod_parse.symbol, prod_parse.measure.amount, prod_parse.measure.units, prod_parse.intermediate)  # pylint: disable=C0301

            closure.products.append(
                Product(
                    loc = textx.get_location(prod_parse),
                    symbol = prod_parse.symbol,
                    amount = Measure(
                        amount = prod_parse.measure.amount,
                        units = prod_parse.measure.units,
                    ),
                    intermediate = (prod_parse.intermediate == "INTERMEDIATE"),
                )
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
Accessor for the total duration of one Bwyd module.
        """
        total_sec: int = int(sum([  # type: ignore  # pylint: disable=R1728
            op.get_duration().normalize()
            for closure in self.closures.values()
            for focus in closure.foci
            for activity in focus.activities
            for op in activity.ops
        ]))

        return Duration(total_sec, "sec").humanize()


    def total_yields (
        self,
        ) -> typing.List[ str ]:
        """
Accessor for the total, non-intermediate yields of one Bwyd module.
        """
        return [
            product
            for closure in self.closures.values()
            for product in closure.total_yields()
        ]


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
