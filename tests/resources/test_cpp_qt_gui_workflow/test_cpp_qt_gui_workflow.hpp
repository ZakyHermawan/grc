#ifndef TEST_CPP_QT_GUI_WORKFLOW_HPP
#define TEST_CPP_QT_GUI_WORKFLOW_HPP
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
#include <gnuradio/blocks/throttle.h>
#include <string_view>
#include <algorithm>
#include <gnuradio/qtgui/time_sink_c.h>

#include <QVBoxLayout>
#include <QScrollArea>
#include <QWidget>
#include <QGridLayout>
#include <QSettings>
#include <QApplication>


using namespace gr;


class test_cpp_qt_gui_workflow : public QWidget {
    Q_OBJECT

private:
    QVBoxLayout *top_scroll_layout;
    QScrollArea *top_scroll;
    QWidget *top_widget;
    QVBoxLayout *top_layout;
    QGridLayout *top_grid_layout;
    QSettings *settings;


    qtgui::time_sink_c::sptr qtgui_time_sink_x_0;
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
    analog::sig_source_c::sptr analog_sig_source_x_0;


// Variables:
    long samp_rate = 32000;

public:
    top_block_sptr tb;
    test_cpp_qt_gui_workflow();
    ~test_cpp_qt_gui_workflow();

    long get_samp_rate () const;
    void set_samp_rate(long samp_rate);

};

#endif

