#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a corpus of Bywd modules into HTML.
"""

import pathlib

from icecream import ic
import bwyd


if __name__ == "__main__":
    corpus: bwyd.Corpus = bwyd.Corpus()
    examples_path: pathlib.Path = pathlib.Path("examples")

    count: int = corpus.render_html_files(
        examples_path,
        #glob = "bread*.bwyd",
        debug = True, # False
    )

    ic(count)
