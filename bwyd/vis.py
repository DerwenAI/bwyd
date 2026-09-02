#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from enum import StrEnum
import os
import pathlib
import tempfile
import typing

import rdflib

import xandergraph as xg


class Style(StrEnum):
    SUPER = "bwyd:Super"
    KEYWORD = "bwyd:Keyword"
    INGREDIENT = "bwyd:Ingredient"
    PRODUCT = "bwyd:Product"
    RECIPE = "bwyd:Recipe"
    CLOSURE = "bwyd:Closure"
    CQ = "bwyd:CompetencyQuestion"
    OTHER = "other"


class Visualization:
    """
The baseline visualization class shows an interactive view of the 
search/pantry terms, recipes, and products.
    """

    ## https://visjs.github.io/vis-network/docs/network/
    ## ellipse, circle, box, text
    ## diamond, dot, star, triangle, triangleDown, hexagon, square,

    NODE_STYLES: dict[ Style, xg.NodeStyle ] = {
        Style.SUPER: xg.NodeStyle(
            color = "#c45335",
            shape = "box",
            show_label = True,
        ),

        Style.KEYWORD: xg.NodeStyle(
            color = "#cc7a3d",
            shape = "box",
            show_label = True,
        ),

        Style.INGREDIENT: xg.NodeStyle(
            color = "#e6c994",
            shape = "box",
            show_label = True,
        ),

        Style.PRODUCT: xg.NodeStyle(
            color = "#fbf2c4",
            shape = "box",
            show_label = True,
        ),

        Style.RECIPE: xg.NodeStyle(
            color = "#74a892",
            shape = "box",
            show_label = True,
        ),

        Style.CLOSURE: xg.NodeStyle(
            color = "#008585",
            shape = "triangle",
        ),

        Style.CQ: xg.NodeStyle(
            color = "#667762",
            shape = "star",
        ),

        Style.OTHER: xg.NodeStyle(
            color = "rgba(250, 250, 250, 0.1)",
            shape = "dot",
        ),
    }


    def __init__ (
        self,
        kg: xg.KnowledgeGraph,
        ) -> None:
        """
Constructor.
        """
        self.kg: xg.KnowledgeGraph = kg
        self.vis: xg.VisHTML = xg.VisHTML()


    def iter_nodes (
        self,
        counter: Counter,
        thesaurus: dict[ str, str ],
        ) -> typing.Iterator[tuple[ str, dict ]]:
        """
Iterator for the stylized nodes in the visualized graph.
        """
        for iri, attrs in self.kg.pg.nodes(data = True):
            if iri in thesaurus:
                node: dict = {}

                node["style"] = self.NODE_STYLES[thesaurus[iri]]
                node["size"] = 2
                show_label: bool = self.NODE_STYLES[thesaurus[iri]].show_label

                node["label"] = ""
                node["title"] = ""

                if show_label or True:
                    node["size"] = 10

                    if "dcterms:title" in attrs:
                        node["label"] = attrs.get("dcterms:title")["en"]
                    elif "skos:prefLabel" in attrs:
                        node["label"] = attrs.get("skos:prefLabel")["en"]
    
                    if "skos:definition" in attrs:
                        node["title"] = attrs.get("skos:definition")["en"]
                    else:
                        node["title"] = iri

                if thesaurus[iri] == "bwyd:Closure":
                    label: str = iri.replace("<", "").replace(">", "").split(":")[-1].replace("closure", "")
                    node["label"] = label

                counter[thesaurus[iri]] += 1
                yield iri, node


    def iter_edges (
        self,
        counter: Counter,
        ) -> typing.Iterator[tuple[ str, str, str ]]:
        """
Iterator for the stylized edges in the visualized graph.
        """
        for src_iri, dst_iri, key in self.kg.pg.edges(keys = True):
            rel: str = self.kg.pg.edges[src_iri, dst_iri, key]["rel"]
            counter[rel] += 1
            yield src_iri, dst_iri, rel


    def gen_html (
        self,
        ) -> str:
        """
Generate optimized HTML for the given `Vis.JS` graph.
        """
        query: str = f"""
SELECT DISTINCT ?thing ?kind
WHERE {{
    ?thing a ?kind .
}}""".strip()

        ns: rdflib.namespace.NamespaceManager = self.kg.get_ns()

        thesaurus: dict[ str, str ] = {
            thing.n3(ns): kind.n3(ns)
            for thing, kind in self.kg.graph.query(query)
            if kind.n3(ns).startswith("bwyd:")
        }

        temp_file: tempfile._TemporaryFileWrapper = tempfile.NamedTemporaryFile(
            mode = "w",
            encoding = "utf-8",
            suffix = ".html",
            delete = False,
            delete_on_close = False,
        )

        html_path: pathlib.Path = pathlib.Path(temp_file.name)
        counter_nodes: Counter = Counter()
        counter_edges: Counter = Counter()

        self.vis.gen_vis_html(
            html_path,
            self.iter_nodes(counter_nodes, thesaurus),
            self.iter_edges(counter_edges),
            height = "900px",
            width = "100%",
        )

        temp_file.close()

        node_meta: dict = {
            kind: {
                "count": count,
                "color": self.NODE_STYLES[kind].color,
            }
            for kind, count in sorted(counter_nodes.items(), key = lambda x: x[1], reverse = True)
        }

        edge_meta: dict = {
            kind: {
                "count": count,
            }
            for kind, count in sorted(counter_edges.items(), key = lambda x: x[1], reverse = True)
        }

        self.vis.rebuild_html(
            html_path,
            html_path,
            node_meta,
            edge_meta,
        )

        html: str = html_path.read_text()
        temp_file.close()
        os.unlink(temp_file.name)

        return html
