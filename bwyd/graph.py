#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Knowledge Graph support for the Bwyd language.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import urllib.parse

import rdflib

from .resources import BWYD_NAMESPACE


######################################################################
## knowledge graph management

class Graph:
    """
A knowledge graph based on a corpus of Bwyd modules.
    """
    def __init__ (
        self,
        ) -> None:
        """
Constructor.
        """
        self.lang: str = "en"
        self.prefix: str = "bwyd"
        self.ns_bwyd: rdflib.Namespace = rdflib.Namespace(BWYD_NAMESPACE)
        self.graph: rdflib.Graph = rdflib.Graph()

        nm: rdflib.namespace.NamespaceManager = self.graph.namespace_manager
        nm.bind(self.prefix, self.ns_bwyd)


    def compose_iri (
        self,
        names: list[ str ],
        ) -> rdflib.URIRef:
        """
Compose an IRI in the Bwyd namespace.
        """
        urn: str = ":".join([ urllib.parse.quote_plus(name) for name in names ])
        return rdflib.URIRef(self.ns_bwyd + urn)


    def compose_iri_instance (
        self,
        inst_symbol: str,
        *,
        sub_symbol: str | None = None,
        ) -> rdflib.URIRef:
        """
Compose an IRI in the Bwyd namespace for an instance of a class.
        """
        if sub_symbol is not None:
            return rdflib.URIRef(self.ns_bwyd + inst_symbol + "#" + sub_symbol)

        return rdflib.URIRef(self.ns_bwyd + inst_symbol)


    def compose_iri_literal (
        self,
        literal: str,
        *,
        lang: str,
        ) -> rdflib.Literal:
        """
Compose an IRI in the Bwyd namespace for a literal.
        """
        return rdflib.Literal(
            literal,
            lang = lang,
        )


    def add_tuple (
        self,
        s_obj: rdflib.URIRef,
        p_obj: rdflib.URIRef,
        o_obj: rdflib.term.Identifier,
        ) -> None:
        """
Add one RDF tuple to the graph.
        """
        self.graph.add(( s_obj, p_obj, o_obj, ))


    def serialize (
        self,
        *,
        format: str = "turtle",  # pylint: disable=W0622
        ) -> str:
        """
Return the serialized graph int the given format.
        """
        return self.graph.serialize(
            format = format,
            base = BWYD_NAMESPACE,
        )
