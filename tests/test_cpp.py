# Copyright 2019 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import pytest

from argparse import Namespace
from os import path
import tempfile

from gnuradio_companion.compiler import main


def test_cpp(capsys):
    args = Namespace(
        output=tempfile.gettempdir(),
        user_lib_dir=False,
        grc_files=[
            path.join(
                path.dirname(__file__), 'resources', 'test_cpp.grc'
            ),
            path.join(
                path.dirname(__file__), 'resources', 'test_cpp_mako.grc'
            ),
            path.join(
                path.dirname(__file__), 'resources', 'test_cpp_jinja.grc'
            ),

        ],
        run=True
    )

    main(args)

    out, err = capsys.readouterr()
    assert not err
