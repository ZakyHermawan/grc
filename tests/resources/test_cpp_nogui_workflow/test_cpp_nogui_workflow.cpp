/********************
GNU Radio C++ Flow Graph Source File

Title: Not titled yet
Author: rootkid
GNU Radio version: v3.11.0.0git-792-gd3eb57d0
********************/

#include "test_cpp_nogui_workflow.hpp"

using namespace gr;


test_cpp_nogui_workflow::test_cpp_nogui_workflow ()  {


    this->tb = gr::make_top_block("Not titled yet");

// Blocks:
        this->blocks_throttle2_0 = blocks::throttle::make(sizeof(gr_complex) * 1, samp_rate, true, blocks_throttle2_0_limit(0.1));

        this->blocks_null_sink_0 = blocks::null_sink::make(sizeof(gr_complex)*1);

        this->analog_sig_source_x_0 = analog::sig_source_c::make(samp_rate, analog::GR_COS_WAVE, 1000, 1, 0,0);


// Connections:
    this->tb->hier_block2::connect(this->analog_sig_source_x_0, 0, this->blocks_throttle2_0, 0);
    this->tb->hier_block2::connect(this->blocks_throttle2_0, 0, this->blocks_null_sink_0, 0);
}

test_cpp_nogui_workflow::~test_cpp_nogui_workflow () {
}

// Callbacks:
long test_cpp_nogui_workflow::get_samp_rate () const {
    return this->samp_rate;
}

void test_cpp_nogui_workflow::set_samp_rate (long samp_rate) {
    this->samp_rate = samp_rate;
    this->analog_sig_source_x_0->set_sampling_freq(this->samp_rate);
    this->blocks_throttle2_0->set_sample_rate(this->samp_rate);
}


int main (int argc, char **argv) {

    test_cpp_nogui_workflow* top_block = new test_cpp_nogui_workflow();
    top_block->tb->start();
    std::cout << "Press Enter to quit: ";
    std::cin.ignore();
    top_block->tb->stop();
    top_block->tb->wait();


    return 0;
}
