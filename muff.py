#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib
import typing

from icecream import ic
import requests_cache

import bwyd


if __name__ == "__main__":
    dsl: bwyd.Bwyd = bwyd.Bwyd(
        config_path = pathlib.Path("config.toml"),
    )

    corpus: bwyd.Corpus = dsl.build_corpus()
    session: requests_cache.CachedSession = corpus.get_cache()

    examples_path: pathlib.Path = pathlib.Path("examples")

    modules: typing.List[ bwyd.Module ] = corpus.render_html_files(
        examples_path,
        #glob = "bread*.bwyd",
        glob = "app*.bwyd",
        debug = True, # False
    )

    mod_data: dict = {
        "corpus": {
            "icon": bwyd.BWYD_SVG,
            "modules": [
                {
                    "slug": module.slug,
                    "thumb": module.get_thumbnail(session),
                    "title": module.title,
                    "text": module.text,
                    "serves": module.total_yields(),
                    "duration": module.total_duration(),
                    "updated": module.updated,
                }
                for module in modules
            ],
        },
    }

    #ic(mod_data)

    html: str = bwyd.JINJA_INDEX_TEMPLATE.render(mod_data)

    with open(examples_path / "index.html", "w", encoding = "utf-8") as fp:
        fp.write(html)
