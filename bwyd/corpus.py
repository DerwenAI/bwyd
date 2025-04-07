#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manage a corpus as a directory of Bwyd modules.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import pathlib

from icecream import ic  # type: ignore  # pylint: disable=E0401

from .module import Module
from .parser import Bwyd


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


    def render_html_files (
        self,
        dir_path: pathlib.Path,
        *,
        glob: str = "*.bwyd",
        suffix: str = ".html",
        debug: bool = False,
        ) -> int:
        """
Traverse the given directory, rendering Bwyd scripts as HTML in place.
Return a count of the modules processed.
        """
        count: int = 0

        for bwyd_path in dir_path.rglob(glob):
            slug: str = bwyd_path.stem

            # filter out checkpoint files, if any
            # WHERE DO THESE COME FROM?
            if slug.endswith("-checkpoint"):
                continue

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

            # render HTML using the Jinja2 template
            html_path: pathlib.Path = bwyd_path.with_suffix(suffix)

            with open(html_path, "w", encoding = "utf-8") as fp:
                fp.write(module.render_template())

            count += 1

        return count
