#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jupyter wrapper kernel for Bwyd
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from ipykernel.kernelapp import IPKernelApp  # pylint: disable=E0401
from ipykernel.kernelbase import Kernel  # pylint: disable=E0401


class BwydKernel (Kernel):  # pylint: disable=R0903
    """
Jupyter wrapper kernel
    """
    banner = "Bwyd kernel -- DSL for cooking"

    implementation_version = "0.2"
    implementation = "Bwyd"

    language_version = "0.1"
    language = "no-op"

    language_info = {
        "name": "Any text",
        "mimetype": "text/plain",
        "file_extension": ".bwyd",
    }


    def do_execute (  # pylint: disable=R0913
        self,
        code,
        silent,
        store_history = True,  # pylint: disable=W0613
        user_expressions = None,  # pylint: disable=W0613
        allow_stdin = False,  # pylint: disable=W0613
        ) -> dict:
        """
Simply echo any given input to `stdout`
        """
        if not silent:
            self.send_response(
                self.iopub_socket,
                "stream",
                {
                    "name": "stdout",
                    "text": code,
                }
            )

        return {
            "status": "ok",
            "execution_count": self.execution_count, # base class increments execution count
            "payload": [],
            "user_expressions": {},
        }


if __name__ == "__main__":
    IPKernelApp.launch_instance(kernel_class = BwydKernel)
