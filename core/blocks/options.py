from . import Block, register_build_in
from ._templates import MakoTemplates
from ._build import build_params
from ..base import Element

from collections import OrderedDict, defaultdict

templates = MakoTemplates()

@register_build_in
class Options(Block):
    """
    Implementation of Options block for codegen purpose
    This block will be used to select workflow and provide informations for code generator
    """
    key = 'options' # block id
    label = 'Options' # block name

    parameters_data = build_params(
        params_raw=[
            dict(id='title',
                label='Title',
                dtype='string',
                hide="${ ('none' if title else 'part') }",
            ),
            dict(id='author',
                label='Author',
                dtype='string',
                hide="${ ('none' if author else 'part') }",
            ),
            dict(id='copyright',
                label='Copyright',
                dtype='string',
                hide="${ ('none' if copyright else 'part') }",
            ),
            dict(id='description',
                label='description',
                dtype='string',
                hide="${ ('none' if description else 'part') }",
            ),
            dict(id='output_language',
                label='Output Language',
                dtype='enum',
                default='python',
                options=['python'],
                option_labels=['Python'],
                option_attributes=defaultdict(dict), # delete soon, i think its unnecessary
                hide="${ ('none' if generate_options else 'part') }",
            ),
            dict(id='generate_options',
                label='Generate Options',
                dtype='enum',
                default='qt_gui',
                options=['qt_gui', 'bokeh_gui'],
                option_labels=['QT GUI', 'Bokeh GUI'],
            ),
            dict(id='gen_linking',
                label='Linking',
                dtype='enum',
                default='dynamic',
                options=['dynamic', 'static'],
                option_labels=['dynamic', 'static'],
                hide="all",
            ),
            dict(id='gen_cmake',
                label='Generate CMakeLists.txt',
                dtype='enum',
                default='On',
                options=['On', 'Off'],
                hide="${ ('part' if output_language == 'cpp' else 'all') }",
            ),
            dict(id='cmake_opt',
                label='CMake options',
                dtype='string',
                default='',
                hide="${ ('part' if output_language == 'cpp' else 'all') }",
            ),
            dict(id='category',
                label='Category',
                dtype='string',
                default='[GRC Hier Block]',
                hide=" ${ ('none' if generate_options.startswith('hb') else 'all') }",
            ),
            dict(id='run_options',
                label='Run Options',
                dtype='enum',
                default='prompt',
                options=['run', 'prompt'],
                option_labels=['Run to Completion', 'Prompt for Exit'],
                hide="${ ('none' if generate_options == 'no_gui' else 'all') }",
            ),
            dict(id='placement',
                label='Widget Placement',
                dtype='int_vector',
                default='(0, 0)',
                hide="${ ('part' if generate_options == 'bokeh_gui' else 'all') }",
            ),
            dict(id='window_size',
                label='Window Size',
                dtype='int_vector',
                default='(1000, 1000)',
                hide="${ ('part' if generate_options == 'bokeh_gui' else 'all') }",
            ),
            dict(id='sizing_mode',
                label='Sizing Mode',
                dtype='enum',
                default='fixed',
                options=['fixed', 'stretch_both', 'scale_width', 'scale_height', 'scale_both'],
                option_labels=['Fixed', 'Stretch Both', 'Scale Width', 'Scale Height', 'Scale Both'],
                hide="${ ('part' if generate_options == 'bokeh_gui' else 'all') }",
            ),
            dict(id='run',
                label='Run',
                dtype='bool',
                default='True',
                options=['True', 'False'],
                option_labels=['Autostart', 'off'],
                hide="${ ('all' if generate_options not in ('qt_gui', 'bokeh_gui') else ('part' if run else 'none')) }",
            ),
            dict(id='max_nouts',
                label='Max Number of Output',
                dtype='int',
                default='0',
                hide=" ${ ('all' if generate_options.startswith('hb') else ('none' if max_nouts else 'part')) }",
            ),
            dict(id='realtime_scheduling',
                label='Realtime Scheduling',
                dtype='enum',
                options=['', '1'],
                option_labels=['Off', 'On'],
                hide="${ ('all' if generate_options.startswith('hb') else ('none' if realtime_scheduling else 'part')) }",
            ),
            dict(id='qt_qss_theme',
                label='QSS Theme',
                dtype='file_open',
                hide="${ ('all' if generate_options != 'qt_gui' else ('none' if qt_qss_theme else 'part')) }",
            ),
            dict(id='thread_safe_setters',
                label='Thread-safe setters',
                category='Advanced',
                dtype='enum',
                options=['', '1'],
                option_labels=['Off', 'On'],
                hide="part",
            ),
            dict(id='catch_exceptions',
                label='Catch Block Exceptions',
                category='Advanced',
                dtype='enum',
                default='True',
                options=['False', 'True'],
                option_labels=['Off', 'On'],
                hide="part",
            ),
            dict(id='run_command',
                label='Run Command',
                category='Advanced',
                dtype='string',
                default=r'{python} -u {filename}',
                options=['', '1'],
                option_labels=['Off', 'On'],
                hide="${ ('all' if generate_options.startswith('hb') else 'part') }",
            ),
            dict(id='hier_block_src_path',
                label='Hier Block Source Path',
                category='Advanced',
                dtype='string',
                options='.:',
                hide="part",
            ),
            dict(id='generator_class_name',
                dtype='string',
                hide="all"
            ),
        ],
        have_inputs=False,
        have_outputs=False,
        flags=Block.flags,
        block_id=key,
    )

    cpp_templates = MakoTemplates(includes=['#include <gnuradio/top_block.h>'])
    file_format = 1

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_platform = parent.parent_platform
        self.workflows = self.parent_platform.workflow_manager.workflows # get all available workflow objects
        self.codegen_options = dict() # key: output_language, val: list of generator_options
        self.parse_workflows()

        default_output_language = self.params['output_language']

        tmp_dct = OrderedDict()
        tmp_dct.attributes = defaultdict(dict)
        for output_language, output_language_label in self.codegen_options.keys():
            tmp_dct[output_language] = output_language_label
        default_output_language.options = tmp_dct
        self.params['output_language'] = default_output_language

        self.asserts.extend([
            "len({placement}) == 4 or len({placement}) == 2".format(placement=self.params['placement'].get_value()),
            "all(i >= 0 for i in {placement})".format(placement=self.params['placement'].get_value()),
        ])

        self.update_params_based_on_generate_options()
        self.update_params_based_on_run()

        self.templates['imports'] = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(
            "from gnuradio import gr",
            "from gnuradio.filter import firdes",
            "from gnuradio.fft import window",
            "import sys",
            "import signal",
            r"% if generate_options == 'qt_gui':",
            "from PyQt5 import Qt",
            r"% endif",
            r"% if not generate_options.startswith('hb'):",
            "from argparse import ArgumentParser",
            "from gnuradio.eng_arg import eng_float, intx",
            "from gnuradio import eng_notation",
            r"% endif",
        )


    def insert_grc_parameters(self, grc_parameters):
        """
        Update parameters with values from the grc file
        Args:
            grc_parameters (str): option block parameter values from grc
        """
        self.params['title'].value = grc_parameters.get('title', 'Not titled yet')
        self.params['author'].value = grc_parameters.get('author', '')
        self.params['copyright'].value = grc_parameters.get('copyright', '')
        self.params['description'].value = grc_parameters.get('description', '')
        self.params['output_language'].value = grc_parameters.get('output_language', 'python')
        self.params['generate_options'].value = grc_parameters.get('generate_options', 'qt_gui')
        self.params['gen_linking'].value = grc_parameters.get('gen_linking', 'dynamic')
        self.params['gen_cmake'].value = grc_parameters.get('gen_cmake', 'On')
        self.params['cmake_opt'].value = grc_parameters.get('cmake_opt', '')
        self.params['category'].value = grc_parameters.get('category', '[GRC Hier Blocks]')
        self.params['run_options'].value = grc_parameters.get('run_options', 'prompt')
        self.params['placement'].value = grc_parameters.get('placement', '(0, 0)')
        self.params['window_size'].value = grc_parameters.get('window_size', '(1000, 1000)')
        self.params['sizing_mode'].value = grc_parameters.get('sizing_mode', 'fixed')
        self.params['run'].value = grc_parameters.get('run', 'True')
        self.params['max_nouts'].value = grc_parameters.get('max_nouts', '0')
        self.params['realtime_scheduling'].value = grc_parameters.get('realtime_scheduling', '')
        self.params['qt_qss_theme'].value = grc_parameters.get('qt_qss_theme', '')
        self.params['thread_safe_setters'].value = grc_parameters.get('thread_safe_setters', '')
        self.params['catch_exceptions'].value = grc_parameters.get('catch_exceptions', 'True')
        self.params['run_command'].value = grc_parameters.get('run_command', r'{python} -u {filename}')
        self.params['hier_block_src_path'].value = grc_parameters.get('hier_block_src_path', '.:')
        self.parent.validate() # validiate the flow graph

    def update_params_based_on_generate_options(self) -> None:
        current_generate_options = self.params['generate_options'].get_value()
        if current_generate_options.startswith('hb'):
            self.params['category'].hide = 'none'
            self.params['max_nouts'].hide = 'all'
        else:
            self.params['category'].hide = 'all'
            self.params['max_nouts'].hide = 'none' if self.params['max_nouts'].get_value() != '0' else 'part'
    
    def update_params_based_on_run(self) -> None:
        self.templates['callbacks'] = [
            "if ${}: self.start()\nelse: self.stop(); self.wait()".format(self.params['run'].get_value())
        ]

    def rewrite(self, updated_language='') -> None:
        """
        Update generated_options each time the value of output_language is changed
        Update category parameter
        Args:
            updated_language (str): used to update generate_options param based on updated output language
        """
        Element.rewrite(self)

        choosen_language = updated_language if updated_language else self.params['output_language'].value
        output_language_pair = ()
        for output_language, output_language_label in self.codegen_options.keys():
            if choosen_language == output_language or choosen_language == output_language_label:
              output_language_pair = (output_language, output_language_label)
              break

        list_of_generated_options_pair = self.codegen_options[output_language_pair]

        tmp = OrderedDict()
        tmp.attributes = defaultdict(dict)
        for generated_options, generated_options_label in list_of_generated_options_pair:
            tmp[generated_options] = generated_options_label
        self.params['generate_options'].options = tmp
        self.update_params_based_on_generate_options()
        self.update_params_based_on_run()
        self.update_generator_class()
        super().rewrite()

    def parse_workflows(self) -> None:
        """
        Read all workflow yml file
        for each workflow, use pair for output_language, generator_options and their label
        then, put it on codegen_options

        structure of codegen_options will be
        codegen_options = {
            ...
            (output_language, output_language_label): [(generated_options, generated_options_label), ..]
        }
        """
        for workflow in self.workflows:
            output_language_pair = (workflow.output_language, workflow.output_language_label)
            generator_options_pair = (workflow.generator_options, workflow.generator_options_label)
            if output_language_pair not in self.codegen_options.keys():
                self.codegen_options[output_language_pair] = []
            if generator_options_pair not in self.codegen_options[output_language_pair]:
                self.codegen_options[output_language_pair].append(generator_options_pair)

    def update_generator_class(self) -> None:
        for workflow in self.workflows:
            if workflow.output_language == self.params['output_language'].get_value() \
                and workflow.generator_options == self.params['generate_options'].get_value():
                self.params['generator_class_name'].set_value(workflow.generator_class)
                self.generator_class_name = workflow.generator_class
                return
