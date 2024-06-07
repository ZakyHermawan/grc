#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: rootkid
# GNU Radio version: v3.11.0.0git-792-gd3eb57d0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
import bokehgui



class test_python_bokeh_gui_workflow(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.plot_lst = []
        self.widget_lst = []

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################

        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)




def main(top_block_cls=test_python_bokeh_gui_workflow, options=None):
    # Create Top Block instance
    tb = top_block_cls()

    try:
        tb.start()

        bokehgui.utils.run_server(tb, sizing_mode = "fixed",  widget_placement =  (0, 0), window_size =  (1000, 1000))
    finally:
        tb.logger.info("Exiting the simulation. Stopping Bokeh Server")
        tb.stop()
        tb.wait()


if __name__ == '__main__':
    main()
