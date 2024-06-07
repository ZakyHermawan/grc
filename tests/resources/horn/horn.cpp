/********************
GNU Radio C++ Flow Graph Source File

Title: horn
GNU Radio version: v3.11.0.0git-792-gd3eb57d0
********************/

#include "horn.hpp"

using namespace gr;


horn::horn ()
: QWidget() {

    this->setWindowTitle("horn");
    // check_set_qss
    // set icon
    this->top_scroll_layout = new QVBoxLayout();
    this->setLayout(this->top_scroll_layout);
    this->top_scroll = new QScrollArea();
    this->top_scroll->setFrameStyle(QFrame::NoFrame);
    this->top_scroll_layout->addWidget(this->top_scroll);
    this->top_scroll->setWidgetResizable(true);
    this->top_widget = new QWidget();
    this->top_scroll->setWidget(this->top_widget);
    this->top_layout = new QVBoxLayout(this->top_widget);
    this->top_grid_layout = new QGridLayout();
    this->top_layout->addLayout(this->top_grid_layout);

    this->settings = new QSettings("GNU Radio", "horn");

    this->tb = gr::make_top_block("horn");

// Blocks:
        this->blocks_null_source_0 = blocks::null_source::make(sizeof(gr_complex)*1);

        this->blocks_null_sink_0 = blocks::null_sink::make(sizeof(gr_complex)*1);


// Connections:
    this->tb->hier_block2::connect(this->blocks_null_source_0, 0, this->blocks_null_sink_0, 0);
}

horn::~horn () {
}

// Callbacks:
long horn::get_samp_rate () const {
    return this->samp_rate;
}

void horn::set_samp_rate (long samp_rate) {
    this->samp_rate = samp_rate;
}


int main (int argc, char **argv) {

    QApplication app(argc, argv);

    horn* top_block = new horn();

    top_block->tb->start();
    top_block->show();
    app.exec();


    return 0;
}
#include "moc_horn.cpp"
