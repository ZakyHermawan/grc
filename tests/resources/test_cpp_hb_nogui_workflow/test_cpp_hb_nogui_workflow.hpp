#ifndef TEST_CPP_HB_NOGUI_WORKFLOW_HPP
#define TEST_CPP_HB_NOGUI_WORKFLOW_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: Not titled yet
Author: rootkid
GNU Radio version: v3.11.0.0git-792-gd3eb57d0
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/analog/sig_source.h>
#include <gnuradio/blocks/null_sink.h>
#include <gnuradio/blocks/throttle.h>
#include <string_view>
#include <algorithm>



using namespace gr;


class test_cpp_hb_nogui_workflow : public hier_block2 {

private:


    constexpr unsigned int blocks_throttle2_0_limit(float value) {
      const std::string_view limited("auto");
      if(limited == "time") {
        return std::max(static_cast<unsigned int>(value * samp_rate), 1U);
      } else if (limited == "items") {
        return std::max(static_cast<unsigned int>(value), 1U);
      }
      return 0;
    }
    blocks::throttle::sptr blocks_throttle2_0;
    blocks::null_sink::sptr blocks_null_sink_0;
    analog::sig_source_c::sptr analog_sig_source_x_0;


// Variables:
    long samp_rate = 32000;

public:
    typedef std::shared_ptr<test_cpp_hb_nogui_workflow> sptr;
    static sptr make();
    test_cpp_hb_nogui_workflow();
    ~test_cpp_hb_nogui_workflow();

    long get_samp_rate () const;
    void set_samp_rate(long samp_rate);

};






test_cpp_hb_nogui_workflow::test_cpp_hb_nogui_workflow () : hier_block2("Not titled yet",
                gr::io_signature::make(0, 0, 0),
                gr::io_signature::make(0, 0, 0)
        ) {


// Blocks:
    {
        this->blocks_throttle2_0 = blocks::throttle::make(sizeof(gr_complex) * 1, samp_rate, true, blocks_throttle2_0_limit(0.1));
    }
    {
        this->blocks_null_sink_0 = blocks::null_sink::make(sizeof(gr_complex)*1);
    }
    {
        this->analog_sig_source_x_0 = analog::sig_source_c::make(samp_rate, analog::GR_COS_WAVE, 1000, 1, 0,0);
    }

// Connections:
    hier_block2::connect(this->analog_sig_source_x_0, 0, this->blocks_throttle2_0, 0);
    hier_block2::connect(this->blocks_throttle2_0, 0, this->blocks_null_sink_0, 0);
}
test_cpp_hb_nogui_workflow::~test_cpp_hb_nogui_workflow () {
}

// Callbacks:
long test_cpp_hb_nogui_workflow::get_samp_rate () const {
    return this->samp_rate;
}

void test_cpp_hb_nogui_workflow::set_samp_rate (long samp_rate) {
    this->samp_rate = samp_rate;
    this->analog_sig_source_x_0->set_sampling_freq(this->samp_rate);
    this->blocks_throttle2_0->set_sample_rate(this->samp_rate);
}

test_cpp_hb_nogui_workflow::sptr
test_cpp_hb_nogui_workflow::make()
{
    return gnuradio::make_block_sptr<test_cpp_hb_nogui_workflow>(
        );
}
#endif

