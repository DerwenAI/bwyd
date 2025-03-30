#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bwyd language exception handling.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""


######################################################################
## exception handling

class BwydParserError (Exception):
    """
General parser exception for the Bwyd language.
    """

    def __init__ (
        self,
        *args,
        **kwargs,
        ) -> None:
        """
Custom exception which notes a Bwyd language discrepancy.
        """
        super().__init__(*args)
        self.symbol = kwargs.get("symbol")
