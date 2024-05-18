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
            options=['qt_gui'],
            option_labels=['QT GUI'],
          ),
        ],
        have_inputs=False,
        have_outputs=False,
        flags=Block.flags,
        block_id=key,
    )

    def __init__(self, parent):
      super().__init__(parent)
      parent_platform = parent.parent_platform

      self.workflows = parent_platform.workflow_manager.workflows # get all available workflow objects
      self.codegen_options = dict() # key: output_language, val: list of generator_options
      self.parse_workflows()

      default_output_language = self.params['output_language']

      tmp_dct = OrderedDict()
      tmp_dct.attributes = defaultdict(dict)
      for output_language, output_language_label in self.codegen_options.keys():
        tmp_dct[output_language] = output_language_label
      default_output_language.options = tmp_dct
      self.params['output_language'] = default_output_language

    def rewrite(self):
        """
        Update generated_options each time the value of output_language is changed
        """
        Element.rewrite(self)

        choosen_language = self.params['output_language'].value
        output_language_pair = ()
        for output_language, output_language_label in self.codegen_options.keys():
            if choosen_language == output_language:
              output_language_pair = (output_language, output_language_label)
              break

        list_of_generated_options_pair = self.codegen_options[output_language_pair]

        tmp = OrderedDict()
        tmp.attributes = defaultdict(dict)
        for generated_options, generated_options_label in list_of_generated_options_pair:
            tmp[generated_options] = generated_options_label
        self.params['generate_options'].options = tmp
        super(Options, self).rewrite()
        # probem: after self.params['generate_options'] get changed, its not getting rendered
        # how to manually render self.params['generate_options']

    def parse_workflows(self):
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

    cpp_templates = MakoTemplates(includes=['#include <gnuradio/topblock.h>'])
    file_format=1
