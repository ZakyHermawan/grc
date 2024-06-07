# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: horn
# GNU Radio version: v3.11.0.0git-792-gd3eb57d0


cmake_minimum_required(VERSION 3.8)
set(CMAKE_CXX_STANDARD 14)

project(horn)

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

find_package(Qt5Widgets REQUIRED)
set(CMAKE_AUTOMOC TRUE)



add_executable(horn horn.cpp)
target_link_libraries(horn
    gnuradio::gnuradio-blocks
    gnuradio::gnuradio-qtgui
)

