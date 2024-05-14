"""
Options Block:
The options block sets special parameters for the flow graph. Only one option block is allowed per flow graph.
Title, author, and description parameters are for identification purposes.
The window size controls the dimensions of the flow graph editor. The window size (width, height) must be between (300, 300) and (4096, 4096).
The generate options controls the type of code generated. Non-graphical flow graphs should avoid using graphical sinks or graphical variable controls.
In a graphical application, run can be controlled by a variable to start and stop the flowgraph at runtime.
The id of this block determines the name of the generated file and the name of the class. For example, an id of my_block will generate the file my_block.py and class my_block(gr....
The category parameter determines the placement of the block in the block selection window. The category only applies when creating hier blocks. To put hier blocks into the root category, enter / for the category.
The Max Number of Output is the maximum number of output items allowed for any block in the flowgraph; to disable this set the max_nouts equal to 0.Use this to adjust the maximum latency a flowgraph can exhibit.
"""
import glob
import yaml

from . import Block, register_build_in
from ..generator import workflow 
from ._templates import MakoTemplates
from ._build import build_params

templates = MakoTemplates()

@register_build_in
class Options(Block):
  print("out")
  def __init__(self, parent):
    print("initialized")
    super().__init__(parent)
    self.workflows = []
    self.output_languages = []
    self.generate_options = []
    self.parse_workflows()

    self.key = 'optionswe' # this will become id of the block
    self.label = 'options'

    self.parameters_data = build_params(
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
# -   id: generate_options
#     label: Generate Options
#     dtype: enum
#     default: qt_gui
#     options: [qt_gui, bokeh_gui, no_gui, hb, hb_qt_gui]
#     option_labels: [QT GUI, Bokeh GUI, No GUI, Hier Block, Hier Block (QT GUI)]
 
        dict(id='generate_options',
          label='Generate Options',
          dtype='enum',
          default='qt_gui',
          options=['qt_gui', 'bokeh_gui', 'no_gui', 'hb', 'hb_qt_gui'],
          option_labels=['QT GUI', 'Bokeh GUI', 'No GUI', 'Hier Block', 'Hier Block (QT GUI)'],
          hide="${ ('none' if generate_options else 'part') }",
        ),
        dict(id='workflow',
          label='Workflow',
          dtype='enum',
          default='python_qt_gui_workflow',
          options=[workflow['id'] for workflow in self.workflows],
          options_labels=[workflow['label'] for workflow in self.workflows]
        ),
      ],
      have_inputs=False,
      have_outputs=False,
      flags=Block.flags,
      block_id=self.key,
    )

  def parse_workflows(self):
    # read all workflow yml file
    # for each workflow, get it's parameters
    workflow_filenames = glob.glob('../../workflows')
    for workflow_filename in workflow_filenames:
      with open (workflow_filename, 'r') as wf:
        current_workflow = yaml.safe_load(wf)
      self.workflows.append(current_workflow)

  def _run_asserts(self, placement):
    if not (len(placement) == 4 or len(placement) == 2):
      self.add.error_message="length of window placement must be 4 or 2 !"
    if not (all(i>=0 for i in placement)):
      self.add.error_message="placement cannot be below 0!"

    imports=templates.get('imports',"""from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal""")
  
  cpp_templates = MakoTemplates(includes=['#include <gnuradio/topblock.h>'])
  file_format=1

  def hide_bokeh_gui_options_if_not_installed(self):
      try:
          import bokehgui
      except ImportError:
          for param in self.parameters_data:
              if param['id'] == 'generate_options':
                  ind = param['options'].index('bokeh_gui')
                  del param['options'][ind]
                  del param['option_labels'][ind]
