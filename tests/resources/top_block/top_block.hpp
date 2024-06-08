#ifndef TOP_BLOCK_HPP
#define TOP_BLOCK_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: Top Block
GNU Radio version: v3.11.0.0git-792-gd3eb57d0
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/blocks/add_const_cc.h>
#include <gnuradio/blocks/null_sink.h>
#include <gnuradio/blocks/vector_source.h>



using namespace gr;


class top_block_ {

private:


    blocks::vector_source_c::sptr blocks_vector_source_x_0;
    blocks::null_sink::sptr blocks_null_sink_0;
    blocks::add_const_cc::sptr blocks_add_const_vxx_0;



public:
    top_block_sptr tb;
    top_block_();
    ~top_block_();


};

#endif

