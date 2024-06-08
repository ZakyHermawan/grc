# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: Top Block
# GNU Radio version: v3.11.0.0git-792-gd3eb57d0


cmake_minimum_required(VERSION 3.8)
set(CMAKE_CXX_STANDARD 14)

project(top_block)

find_package(Gnuradio "3.11" COMPONENTS
    blocks
    fec
    fft
    filter
    analog
    digital
    dtv
    audio
    channels
    pdu
    iio
    qtgui
    trellis
    video-sdl
    vocoder
    wavelet
    zeromq
    network
    soapy
)




add_executable(top_block top_block.cpp)
target_link_libraries(top_block
    gnuradio::gnuradio-blocks
)

