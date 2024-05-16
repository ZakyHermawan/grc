from . import Block, register_build_in
from ._templates import MakoTemplates
from ._build import build_params

templates = MakoTemplates()

@register_build_in
class Options(Block):
  key = 'options'
  label = 'Options'

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
        options=['python', 'cpp', 'asm'],
        option_labels=['Python', 'C++', 'Assembly__'],
        hide="${ ('none' if generate_options else 'part') }",
      ),
      dict(id='generate_options',
        label='Generate Options',
        dtype='enum',
        default='qt_gui',
        options=['qt_gui', 'bokeh_gui', 'no_gui', 'hb', 'hb_qt_gui'],
        option_labels=['QT GUI', 'Bokeh GUI', 'No GUI', 'Hier Block', 'Hier Block (QT GUI)'],
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

    self.workflows = parent_platform.workflow_manager.workflows
    self.codegen_options = dict()
    self.parse_workflows()

    output_language = dict(
      id='output_language',
      label='Output Language',
      dtype='enum',
      default='python',
      options=self.codegen_options.keys(),
      option_labels=self.codegen_options.keys(),
      hide="${ ('none' if generate_options else 'part') }",
    )
    print(self.parameters_data[6])
    self.parameters_data[6] = output_language # how to update this on gui ?
    print(self.parameters_data[6])

  def parse_workflows(self):
    # read all workflow yml file
    # for each workflow, get it's parameters
    for workflow in self.workflows:
      output_language = workflow.output_language
      if output_language not in self.codegen_options.keys():
        self.codegen_options[output_language] = []
      if workflow.generator_options not in self.codegen_options[output_language]:
        self.codegen_options[output_language].append(workflow.generator_options)
  
  cpp_templates = MakoTemplates(includes=['#include <gnuradio/topblock.h>'])
  file_format=1
