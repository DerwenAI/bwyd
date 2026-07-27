#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An example module in the Bwyd language.
"""

import fileinput
import os
import pathlib
import sys
import tempfile
import traceback

from icecream import ic
import rdflib
import xandergraph as xg

import bwyd


if __name__ == "__main__":
    dsl: bwyd.Bwyd = bwyd.Bwyd(
        config_path = pathlib.Path("config.toml"),
    )

    # parse a specific Bwyd module
    account: str = "pacoid"

    content_path: pathlib.Path = pathlib.Path("../bwyd-editor/content")
    slug: str = sys.argv[1]

    recipe: bwyd.Recipe = dsl.parse(
        content_path / f"{slug}.bwyd",
        slug = slug,
        debug = False, # True
    )

    # interpret the parsed module
    recipe.interpret(
        account,
        debug = False, # True
    )

    # set up OTTR templates
    graph_dir: pathlib.Path = pathlib.Path(dsl.config["graph"]["rdf_path"])

    kg: xg.KnowledgeGraph = xg.KnowledgeGraph(
        ns = {
            "bwyd": dsl.config["graph"]["ns"],
        },
    )

    kg.load_stottr(graph_dir / "bwyd.stottr")

    # generate RDF for a module
    rdf_data: str = "\n".join(
        recipe.gen_rdf(
            account,
        )
    )

    kg.gen_ottr_rdf(rdf_data)

    corpus_path: pathlib.Path = graph_dir / "corpus.ttl"

    with open(corpus_path, "w", encoding = "utf-8") as fp:
        ttl: str = kg.graph.serialize(format = "turtle")
        fp.write(ttl)

    # load RDF from outside the DSL
    domain_path: pathlib.Path = graph_dir / "domain.ttl"
    shapes_path: pathlib.Path = graph_dir / "shapes.ttl"
    search_path: pathlib.Path = graph_dir / "search.ttl"
    pantry_path: pathlib.Path = graph_dir / "pantry.ttl"
    entire_path: pathlib.Path = graph_dir / "entire.ttl"
        
    ## check for RDF syntax errors within the generated RDF
    graph: rdflib.Graph = rdflib.Graph()

    tf: tempfile.NamedTemporaryFile = tempfile.NamedTemporaryFile(
        delete = False,
        suffix = ".ttl",
    )

    path_list: list[ pathlib.Path ] = [
        corpus_path,
        search_path,
        pantry_path,
    ]

    for ttl_path in path_list:
        try:
            graph.parse(ttl_path.as_posix())
        except Exception as ex:
            ic(ttl_path)
            traceback.print_exc()

    with open(tf.name, "w", encoding = "utf-8") as fp:
        with fileinput.input(files = path_list, encoding = "utf-8") as stream:
            for line in stream:
                fp.write(line)

    graph = rdflib.Graph()
    graph.parse(tf.name)

    ## SHACL validation
    conforms, results_graph, results_text = kg.run_shacl(
        tf.name,
        shapes_path.as_posix(),
        domain_path.as_posix(),
    )

    if not conforms:
        print(results_text)

    tf.close()
    os.unlink(tf.name)

    ## serialize the entire graph in TTL format
    path_list = [
        domain_path,
        search_path,
        pantry_path,
        corpus_path,
    ]

    for ttl_path in path_list:
        kg.graph.parse(ttl_path.as_posix())

    with open(entire_path, "w", encoding = "utf-8") as fp:
        ttl: str = kg.graph.serialize(format = "turtle")
        fp.write(ttl)
