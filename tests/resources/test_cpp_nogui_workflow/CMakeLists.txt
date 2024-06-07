# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: Not titled yet
# Author: rootkid
# GNU Radio version: v3.11.0.0git-792-gd3eb57d0


cmake_minimum_required(VERSION 3.8)
set(CMAKE_CXX_STANDARD 14)

project(test_cpp_nogui_workflow)

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




add_executable(test_cpp_nogui_workflow test_cpp_nogui_workflow.cpp)
target_link_libraries(test_cpp_nogui_workflow
    gnuradio::gnuradio-blocks
    gnuradio::gnuradio-analog
)

