#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An example module in the Bwyd language.
"""

import json
import pathlib
import sys

from deepdiff import DeepDiff
from icecream import ic

import bwyd


if __name__ == "__main__":
    ic.configureOutput(
        noColor = True,
    )

    content_path: pathlib.Path = pathlib.Path("../bwyd-editor/content")
    account: str = "pacoid"

    corpus: bwyd.Corpus = bwyd.Corpus(
        account,
    )

    ######################################################################
    ## TESTING

    corpus.parse_recipes(content_path)
    corpus.gen_rdf()
    corpus.build_product_graph()

    ######################################################################
    # parse an example Bwyd module

    slug: str = sys.argv[1]

    recipe: bwyd.Recipe = corpus.dsl.parse(
        content_path / f"{slug}.bwyd",
        corpus.converter,
        slug = slug,
        debug = False, # True
    )

    # interpret the parsed module
    recipe.interpret(
        debug = True, # False
    )

    observed: dict = recipe.get_model(
        account,
        keyword_namespace = corpus.keyword_namespace,
        product_map = corpus.product_map,
    )

    # output a JSON model, for use in unit tests
    with open(content_path / f"{slug}.json", "w", encoding = "utf-8") as fp:
        fp.write(json.dumps(
            observed,
            indent = 2,
            sort_keys = False,
        ))

    ######################################################################
    # only go this far

    ic(corpus.render_page_meta(recipe, anchor = ""))

    sys.exit(0)

    # compare with expected results
    with open("expect.json", "r", encoding = "utf-8") as fp:
        expected: dict = json.load(fp)

    ic(DeepDiff(expected, observed))
