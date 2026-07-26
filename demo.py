#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test usage of pyOTTR
"""

import fileinput
import os
import pathlib
import sys
import tempfile

from icecream import ic
import xandergraph as xg
import rdflib


if __name__ == "__main__":
    graph_dir: pathlib.Path = pathlib.Path("graph")

    kg: xg.KnowledgeGraph = xg.KnowledgeGraph(
        ns = {
            "bwyd": "https://github.com/DerwenAI/bwyd/wiki/ns#",
        },
    )

    kg.load_stottr(graph_dir / "bwyd.stottr")

    ## generate models from the data
    rdf_data: str = """
@prefix bwyd:     <https://github.com/DerwenAI/bwyd/wiki/ns#> .

bwyd:Recipe(
  <urn:bwyd:pacoid:panna_cotta> ,
  "Panna Cotta"@en ,
  "A light, creamy dessert which pairs with so many fruits"@en ,
  <https://spdx.org/licenses/CC-BY-NC-SA-4.0> ,
  <https://derwen.ai/paco> ,
  "2022-07-16"^^xsd:dateTime ,
) .

bwyd:RecipeImage(
  <urn:bwyd:pacoid:panna_cotta> ,
  <https://www.instagram.com/p/CgGYEZFL7Dx/> ,
) .

bwyd:RecipeSource(
  <urn:bwyd:pacoid:panna_cotta> ,
  <https://www.thekitchn.com/how-to-make-panna-cotta-cooking-lessons-from-the-kitchn-200070> ,
) .

bwyd:RecipeSource(
  <urn:bwyd:pacoid:panna_cotta> ,
  <https://mytastefulrecipes.com/almond-milk-panna-cotta-recipe/> ,
) .

bwyd:RecipeDepends(
  <urn:bwyd:pacoid:panna_cotta> ,
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
) .

bwyd:RecipeDepends(
  <urn:bwyd:pacoid:panna_cotta> ,
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
) .

bwyd:Closure(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  "mix the cream"@en ,
  "Prepare the cream filling"@en ,
) .

bwyd:ClosureConsumes(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  <urn:bwyd:ingredient:cream> ,
) .

bwyd:ClosureConsumes(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  <urn:bwyd:ingredient:granulated_sugar> ,
) .

bwyd:ClosureProduces(
  <urn:bwyd:pacoid:panna_cotta/closure_1> ,
  <urn:bwyd:pacoid:panna_cotta/closure_1/product/filling> ,
) .


bwyd:Closure(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  "chill in containers"@en ,
  "Fill the ramekins and chill"@en ,
) .

bwyd:ClosureSuper(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  <urn:bwyd:super:dessert> ,
) .

bwyd:ClosureSuper(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  <urn:bwyd:super:pudding> ,
) .

bwyd:ClosureKeyword(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  <urn:bwyd:keyword:italian> ,
) .

bwyd:ClosureConsumes(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  <urn:bwyd:pacoid:panna_cotta/closure_1/product/filling> ,
) .

bwyd:ClosureProduces(
  <urn:bwyd:pacoid:panna_cotta/closure_2> ,
  <urn:bwyd:pacoid:product:panna_cotta> ,
) .


bwyd:Super(
  <urn:bwyd:super:dessert> ,
  "dessert"@en ,
) .

bwyd:Super(
  <urn:bwyd:super:pudding> ,
  "pudding"@en ,
) .


bwyd:Keyword(
  <urn:bwyd:keyword:italian> ,
  "italian"@en ,
) .


bwyd:Product(
  <urn:bwyd:pacoid:panna_cotta/closure_1/product/filling> ,
  "filling"@en ,
) .

bwyd:Product(
  <urn:bwyd:pacoid:product:panna_cotta> ,
  "panna_cotta"@en ,
) .
    """.strip()


    domain_path: pathlib.Path = graph_dir / "domain.ttl"
    search_path: pathlib.Path = graph_dir / "search.ttl"
    pantry_path: pathlib.Path = graph_dir / "pantry.ttl"
    shapes_path: pathlib.Path = graph_dir / "shapes.ttl"

    ## save generated RDF to a file
    kg.gen_ottr_rdf(rdf_data)
    corpus_path: pathlib.Path = graph_dir / "corpus.ttl"

    with open(corpus_path, "w", encoding = "utf-8") as fp:
        ttl: str = kg.graph.serialize(format = "turtle")
        fp.write(ttl)


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
        graph.parse(ttl_path.as_posix())

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
