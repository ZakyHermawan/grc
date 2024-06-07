#ifndef HORN_HPP
#define HORN_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: horn
GNU Radio version: v3.11.0.0git-792-gd3eb57d0
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/blocks/null_sink.h>
#include <gnuradio/blocks/null_source.h>

#include <QVBoxLayout>
#include <QScrollArea>
#include <QWidget>
#include <QGridLayout>
#include <QSettings>
#include <QApplication>


using namespace gr;


class horn : public QWidget {
    Q_OBJECT

private:
    QVBoxLayout *top_scroll_layout;
    QScrollArea *top_scroll;
    QWidget *top_widget;
    QVBoxLayout *top_layout;
    QGridLayout *top_grid_layout;
    QSettings *settings;


    blocks::null_source::sptr blocks_null_source_0;
    blocks::null_sink::sptr blocks_null_sink_0;


// Variables:
    long samp_rate = 32000;

public:
    top_block_sptr tb;
    horn();
    ~horn();

    long get_samp_rate () const;
    void set_samp_rate(long samp_rate);

};

#endif

