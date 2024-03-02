#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI installer for the Bwyd kernel.
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

from ipykernel.kernelapp import IPKernelApp  # pylint: disable=E0401

from .kernel import BwydKernel

IPKernelApp.launch_instance(
    kernel_class = BwydKernel,
)
