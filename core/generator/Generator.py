# Copyright 2008-2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
#


from .hier_block import HierBlockGenerator, QtHierBlockGenerator
from .top_block import TopBlockGenerator
from .cpp_top_block import CppTopBlockGenerator
from .cpp_hier_block import CppHierBlockGenerator
import sys

class Generator(object):
    """Adaptor for various generators (uses generate_options)"""

    def __init__(self, flow_graph, output_dir):
        """
        Initialize the generator object.
        Determine the file to generate.

        Args:
            flow_graph: the flow graph object
            output_dir: the output path for generated files
        """
        self.generate_options = flow_graph.get_option('generate_options')
        self.output_language = flow_graph.get_option('output_language')

        self.generator_class_name = flow_graph.get_option('generator_class_name')
        generator_cls = getattr(sys.modules[__name__], self.generator_class_name)
        
        self._generator = generator_cls(flow_graph, output_dir)

    def __getattr__(self, item):
        """get all other attrib from actual generator object"""
        return getattr(self._generator, item)
