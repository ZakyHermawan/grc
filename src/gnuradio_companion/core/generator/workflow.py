# might be not needed, or maybe workflow parsise on options can be moved to here
import yaml
class Workflow:
  def __init__(self, flow_graph):
    self.flow_graph = flow_graph
    self.generator_class = None
    self.workflow_name = ''
    # self.generate_options = flow_graph.get_option('generate_options')
    # self.output_language = flow_graph.get_option('output_language')

    # if self.output_language == 'Python':
    #   if self.generate_options == 'hb':
    #     self.workflow_name = 'python_hb_nogui.workflow.yml'
    #   elif self.generate_options == 'hb_qt_gui':
    #     self.workflow_name = 'python_hb_qt_gui.workflow.yml'
    #   elif self.generate_options == 'no_gui':
    #     # generator_cls = TopBlockGenerator
    #     self.workflow_name = 'python_nogui.workflow.yml'
    #   elif self.generate_options == 'qt_gui':
    #     self.workflow_name = 'python_qt_gui.workflow.yml'
    #   else:
    #     raise Exception("Unknown workflow")

    # elif self.output_language == 'C++':
    #   if self.generate_options == 'hb':
    #     self.workflow_name = 'cpp_hb_nogui.workflow.yml'
    #   elif self.generate_options == 'hb_qt_gui':
    #     pass
    #   else:
    #     generator_cls = CppTopBlockGenerator
    #     self.workflow_name = ''

    # self._generator = generator_cls(flow_graph, output_dir)


  def get_generator_class(self):
     return self.generator_class
