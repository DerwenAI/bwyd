#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Jupyter kernel installer for Bwyd
see copyright/license https://github.com/DerwenAI/bwyd/README.md
"""

import argparse
import json
import os
import pathlib
import shutil
import sys
import typing

from jupyter_client.kernelspec import KernelSpecManager  # pylint: disable=E0401
from IPython.utils.tempdir import TemporaryDirectory  # pylint: disable=E0401

from .resources import _ICON_PATH


KERNEL_JSON: dict = {
    "argv": [ sys.executable, "-m", "bwyd", "-f", "{connection_file}" ],
    "display_name": "Bwyd",
    "language": "bwyd",
    "codemirror_mode": "shell",
    "env": { "PS1": "$" },
}


def install_my_kernel_spec (
    *,
    user: bool = True,
    prefix: typing.Optional[ str ] = None,
    ) -> None:
    """
Generate a `kernel.json` kernel spec file, then use it to invoke
the Jupyter kernel installer.
    """
    with TemporaryDirectory() as tmp_dir:
        os.chmod(tmp_dir, 0o755) # Starts off as 700, not user readable
        spec_path: str = os.path.join(tmp_dir, "kernel.json")

        with open(spec_path, "w", encoding = "utf-8") as fp:  # pylint: disable=C0103
            json.dump(
                KERNEL_JSON,
                fp,
                sort_keys = True,
            )

        shutil.copyfile(
            _ICON_PATH,
            pathlib.Path(tmp_dir) / _ICON_PATH.name,
        )

        print("Installing IPython kernel spec for Bwyd")

        KernelSpecManager().install_kernel_spec(
            tmp_dir,
            "bwyd",
            user = user,
            prefix = prefix,
        )


def _is_root (
    ) -> bool:
    """
Check whether this is running as a `root` user?
    """
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False # assume not an admin on non-Unix platforms


def main (
    argv = None,
    ) -> None:
    """
Main entry point for the kernel installer.
    """
    parser = argparse.ArgumentParser(
        description = "Install KernelSpec for the Bwyd kernel"
    )

    prefix_locations = parser.add_mutually_exclusive_group()

    prefix_locations.add_argument(
        "--user",
        help = "Install KernelSpec in user\'s home directory",
        action = "store_true",
    )

    prefix_locations.add_argument(
        "--sys-prefix",
        help = "Install KernelSpec in `sys.prefix` which is useful in conda / virtualenv",
        action = "store_true",
        dest = "sys_prefix",
    )

    prefix_locations.add_argument(
        "--prefix",
        help = "Install KernelSpec in this prefix",
        default = None
    )

    args = parser.parse_args(argv)
    user = False
    prefix = None

    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user or not _is_root():
        user = True

    install_my_kernel_spec(
        user = user,
        prefix = prefix,
    )


if __name__ == "__main__":
    main()
