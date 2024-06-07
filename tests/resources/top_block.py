#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 0.0.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block", catch_exceptions=True)

        ##################################################
        # Blocks
        ##################################################

        self.blocks_vector_source_x_0 = blocks.vector_source_c((0, 0, 0), False, 1, [])
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_add_const_vxx_0, 0))





def main(top_block_cls=top_block, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
