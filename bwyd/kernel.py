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
    implementation = "Bwyd"
    implementation_version = "1.0"

    banner = "Bwyd kernel: a DSL for cooking"

    language = "no-op"
    language_version = "1.0"

    language_info = {
        "name": "Bwyd",
        "mimetype": "text/plain",
        "file_extension": ".bwyd",
    }


    def do_execute (  # type: ignore  # pylint: disable=R0913,R0917
        self,
        code,
        silent,
        store_history = True,  # pylint: disable=W0613
        user_expressions = None,  # pylint: disable=W0613
        allow_stdin = False,  # pylint: disable=W0613
        *,
        cell_meta = None,
        cell_id = None,
        ) -> dict:
        """
Simply echo any given input to `stdout`.
See: <https://ipython-books.github.io/16-creating-a-simple-kernel-for-jupyter/>
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


    def do_apply (
        self,
        content,
        bufs,
        msg_id,
        reply_metadata,
        ):
        """DEPRECATED"""
        raise NotImplementedError


if __name__ == "__main__":
    IPKernelApp.launch_instance(kernel_class = BwydKernel)
