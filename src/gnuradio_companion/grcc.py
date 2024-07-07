#!/usr/bin/env python
# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
#

import os
import sys


GR_IMPORT_ERROR_MESSAGE = """\
Cannot import gnuradio.

Is the Python path environment variable set correctly?
    All OS: PYTHONPATH

Is the library path environment variable set correctly?
    Linux: LD_LIBRARY_PATH
    Windows: PATH

See https://wiki.gnuradio.org/index.php/ModuleNotFoundError
"""


def die(error, message):
    msg = "{0}\n\n({1})".format(message, error)
    exit(type(error).__name__ + '\n\n' + msg)


def check_gnuradio_import():
    try:
        from gnuradio import gr
    except ImportError as err:
        die(err, GR_IMPORT_ERROR_MESSAGE)


def run_main():
    script_path = os.path.dirname(os.path.abspath(__file__))
    source_tree_subpath = "src/gnuradio_companion"

    if not script_path.endswith(source_tree_subpath):
        # run the installed version
        from gnuradio_companion.compiler import main
    else:
        print("Running from source tree")
        sys.path.insert(1, script_path[:-len(source_tree_subpath)])
        from gnuradio_companion.compiler import main
    exit(main())

def main():
    check_gnuradio_import()
    run_main()
