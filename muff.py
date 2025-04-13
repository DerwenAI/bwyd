#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib
import typing

from icecream import ic
from jinja2 import Environment, BaseLoader
import bwyd


if __name__ == "__main__":
    corpus: bwyd.Corpus = bwyd.Corpus()
    examples_path: pathlib.Path = pathlib.Path("examples")

    modules: typing.List[ bwyd.Module ] = corpus.render_html_files(
        examples_path,
        #glob = "bread*.bwyd",
        debug = True, # False
    )

    mod_data: dict = {
        "data": [
            {
                "slug": module.slug,
                "title": module.title,
                "thumb": module.get_thumbnail(),
            }
            for module in modules
        ]
    }

    JINJA_INDEX_TEMPLATE: str = """
    <ul>
    {% for module in data %}
      <li>
        <a href="{{ module.slug }}.html"
         >{{ module.title }}</a>
      </li>
    {% endfor %}
    </ul>
    """

    rtemplate = Environment(loader = BaseLoader).from_string(JINJA_INDEX_TEMPLATE)
    html: str= rtemplate.render(mod_data)

    with open(examples_path / "index.html", "w", encoding = "utf-8") as fp:
        fp.write(html)
