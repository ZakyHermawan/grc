/********************
GNU Radio C++ Flow Graph Source File

Title: Top Block
GNU Radio version: v3.11.0.0git-792-gd3eb57d0
********************/

#include "top_block.hpp"

using namespace gr;


top_block_::top_block_ ()  {


    this->tb = gr::make_top_block("Top Block");

// Blocks:
        this->blocks_vector_source_x_0 = blocks::vector_source_c::make((0, 0, 0), false, 1, []);

        this->blocks_null_sink_0 = blocks::null_sink::make(sizeof(gr_complex)*1);

        this->blocks_add_const_vxx_0 = blocks::add_const_cc::make(1);


// Connections:
    this->tb->hier_block2::connect(this->blocks_add_const_vxx_0, 0, this->blocks_null_sink_0, 0);
    this->tb->hier_block2::connect(this->blocks_vector_source_x_0, 0, this->blocks_add_const_vxx_0, 0);
}

top_block_::~top_block_ () {
}

// Callbacks:

int main (int argc, char **argv) {

    top_block_* top_block = new top_block_();
    top_block->tb->start();
    top_block->tb->wait();


    return 0;
}
