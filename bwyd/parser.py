#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DSL implementing the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import configparser
import pathlib
import typing

from icecream import ic  # type: ignore  # pylint: disable=E0401
import textx  # type: ignore  # pylint: disable=E0401

from .module import Module
from .resources import GRAMMAR_PATH


######################################################################
## corpus operations

class Corpus:  # pylint: disable=R0903
    """
A corpus of Bwyd modules.
    """

    def __init__ (
        self,
        *,
        converter: dict = Module.UNIT_CONVERT,
        ) -> None:
        """
Constructor.
        """
        self.converter: dict = converter


    def iter_files (
        self,
        dir_path: pathlib.Path,
        *,
        glob: str = "*.bwyd",
        ) -> typing.Iterator[ pathlib.Path ]:
        """
Iterator for listing the Bwyd modules in a given directory.
        """
        for bwyd_path in dir_path.rglob(glob):
            # filter out checkpoint files, if any
            # WHERE DO THESE COME FROM?
            if not bwyd_path.stem.endswith("-checkpoint"):
                yield bwyd_path


    def render_html_files (
        self,
        dir_path: pathlib.Path,
        *,
        glob: str = "*.bwyd",
        suffix: str = ".html",
        debug: bool = False,
        ) -> typing.List[ Module ]:
        """
Traverse the given directory, rendering Bwyd scripts as HTML in place.
Return a count of the modules processed.
        """
        modules: typing.List[ Module ] = []

        for bwyd_path in self.iter_files(dir_path, glob = glob):
            slug: str = bwyd_path.stem

            if debug:
                ic(bwyd_path.name)

            # parse the Bwyd module
            module: Module = Bwyd.parse(
                bwyd_path,
                slug = slug,
            )

            # interpret the parsed module
            module.interpret(
                debug = debug,
            )

            modules.append(module)

            # render HTML using the Jinja2 template
            html_path: pathlib.Path = bwyd_path.with_suffix(suffix)

            with open(html_path, "w", encoding = "utf-8") as fp:
                fp.write(module.render_template())

        return modules


######################################################################
## parser/interpreter definitions

class Bwyd:  # pylint: disable=R0903
    """
Bwyd DSL parser/interpreter.
    """
    META_MODEL: textx.metamodel.TextXMetaModel = textx.metamodel_from_file(
        GRAMMAR_PATH,
        debug = False, # True
    )


    def __init__ (
        self,
        *,
        config_file: typing.Optional[ pathlib.Path ] = None,
        ) -> None:
        """
Constructor.
        """
        self.config = configparser.ConfigParser()

        if config_file is not None:
            self.config.read(config_file)


    def parse (
        self,
        script: pathlib.Path,
        *,
        slug: typing.Optional[ str ] = None,
        debug: bool = False,
        ) -> Module:
        """
Initialize a parser to load one Bywd module from a file.
        """
        return Module(
            self.META_MODEL.model_from_file(
                script,
                debug = debug,
            ),
            slug = slug,
        )


    def build_corpus (
        self,
        *,
        converter: dict = Module.UNIT_CONVERT,
        ) -> Corpus:
        """
Factory for initializing a corpus of Bywd modules.
        """
        return Corpus(converter = converter)
