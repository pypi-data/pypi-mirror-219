# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

import os
import sys
import warnings

# Remove '' and current working directory from the first entry
# of sys.path, if present to avoid using current directory
# in devpm commands check, freeze, install, list and show,
# when invoked as python -m devpm <command>
if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

# If we are running from a wheel, add the wheel to sys.path
# This allows the usage python devpm-*.whl/devpm install devpm-*.whl
if not __package__ or __package__ == "":
    # __file__ is devpm-*.whl/devpm/__main__.py
    # first dirname call strips of '/__main__.py', second strips off '/devpm'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import devpm
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

if __name__ == "__main__":
    # Work around the error reported in #9540, pending a proper fix.
    # Note: It is essential the warning filter is set *before* importing
    #       devpm, as the deprecation happens at import time, not runtime.
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, module=".*packaging\\.version"
    )
    from devpm._internal.cli.main import main as _main

    sys.exit(_main())
