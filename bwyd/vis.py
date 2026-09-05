#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interactive graph visualization.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from collections import Counter, OrderedDict
from enum import StrEnum
import os
import pathlib
import tempfile
import typing

from icecream import ic  # pylint: disable=W0611
import networkx as nx
import rdflib

import xandergraph as xg  # type: ignore


class Clazz(StrEnum):
    """
Represents styles for the `Vis.JS` library based on the Bwyd taxonomy classes
    """

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

    NODE_STYLES: dict[ str, xg.NodeStyle ] = {
        Clazz.SUPER.value: xg.NodeStyle(
            color = "#c45335",
            shape = xg.NodeShape.DOT.value,
            show_label = True,
        ),

        Clazz.KEYWORD.value: xg.NodeStyle(
            color = "#cc7a3d",
            shape = xg.NodeShape.DOT.value,
            show_label = True,
        ),

        Clazz.INGREDIENT.value: xg.NodeStyle(
            color = "#e6c994",
            shape = xg.NodeShape.BOX.value,
            show_label = True,
        ),

        Clazz.PRODUCT.value: xg.NodeStyle(
            color = "#fbf2c4",
            shape = xg.NodeShape.BOX.value,
            show_label = True,
        ),

        Clazz.RECIPE.value: xg.NodeStyle(
            color = "#74a892",
            shape = xg.NodeShape.BOX.value,
            font_color = "#fff",
            show_label = True,
        ),

        Clazz.CLOSURE.value: xg.NodeStyle(
            color = "#008585",
            shape = xg.NodeShape.TRIANGLE.value,
            size = 3,
            font_size = 6,
        ),

        Clazz.CQ.value: xg.NodeStyle(
            color = "#667762",
            shape = xg.NodeShape.STAR.value,
        ),

        Clazz.OTHER.value: xg.NodeStyle(
            color = "rgba(250, 250, 250, 0.1)",
            shape = xg.NodeShape.DOT.value,
        ),
    }


    def __init__ (
        self,
        kg: xg.KnowledgeGraph,
        radius_max: float = 100.0,
        radius_min: float = 1.0,
        ) -> None:
        """
Constructor.
        """
        self.kg: xg.KnowledgeGraph = kg
        self.vis: xg.VisHTML = xg.VisHTML()
        self.radius_max = radius_max
        self.radius_min = radius_min


    def iter_nodes (
        self,
        counter: Counter,
        thesaurus: dict[ str, str ],
        ) -> typing.Iterator[tuple[ str, dict ]]:
        """
Iterator for the stylized nodes in the visualized graph.
        """
        # calculate centrality
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.load_centrality.html

        rank_orig: OrderedDict = OrderedDict([
            ( iri, cent, )
            for iri, cent in sorted(
                    nx.load_centrality(self.kg.pg).items(),  # type: ignore
                    key = lambda x: x[1],
                    reverse = True,
            )
            if cent > 0.0
        ])

        max_x: float = max(rank_orig.values())
        min_x: float = min(rank_orig.values())
        max_v: float = self.radius_max
        min_v: float = self.radius_min

        rank: OrderedDict = OrderedDict([
            ( iri, (x - min_x) / (max_x - min_x) * (max_v - min_v) + min_v, )
            for iri, x in rank_orig.items()
        ])

        for iri, attrs in self.kg.pg.nodes(data = True):
            if iri in thesaurus:
                show_label: bool = self.NODE_STYLES[thesaurus[iri]].show_label

                node: dict = {
                    "style": self.NODE_STYLES[thesaurus[iri]],
                    "size": self.NODE_STYLES[thesaurus[iri]].size,
                    "value": self.radius_min,
                    "label": "",
                    "title": iri,
                }

                if show_label:
                    if "dcterms:title" in attrs:
                        node["label"] = attrs.get("dcterms:title")["en"]
                    elif "skos:prefLabel" in attrs:
                        node["label"] = attrs.get("skos:prefLabel")["en"]

                    if "skos:definition" in attrs:
                        node["title"] = attrs.get("skos:definition")["en"]

                if thesaurus[iri] in [ Clazz.CLOSURE.value ]:
                    label: str = iri.replace("<", "").replace(">", "").split(":")[-1]
                    node["label"] = label.replace("closure", "")

                elif thesaurus[iri] in [ Clazz.SUPER.value, Clazz.KEYWORD.value ]:
                    if iri in rank:
                        node["value"] = rank[iri]

                elif thesaurus[iri] in [ Clazz.CQ.value ]:
                    continue

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
        query: str = """
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

        temp_file: tempfile._TemporaryFileWrapper = tempfile.NamedTemporaryFile(  # pylint: disable=R1732
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

        html: str = html_path.read_text(encoding = "utf-8")
        temp_file.close()
        os.unlink(temp_file.name)

        return html
