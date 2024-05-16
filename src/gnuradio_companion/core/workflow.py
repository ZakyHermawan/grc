import logging
import yaml

logger = logging.getLogger(__name__)

class Workflow:
  """
  Workflow class is used to parse workflow file
  """
  def __init__(self, *args, **kwargs):
    if len(args) == 1:
      with open(args[0], 'r') as wf:
        self.workflow_params = yaml.safe_load(wf)
    else:
      self.workflow_params = kwargs

    self.id = self.workflow_params.pop('id')
    self.label = self.workflow_params.pop('label')
    self.descripion = self.workflow_params.pop('description')
    self.output_language = self.workflow_params.pop('output_language')
    self.generator_class = self.workflow_params.pop('generator_class')
    self.generator_options = self.workflow_params.pop('generator_options')
    self.context = self.workflow_params # additional workflow parameters


class WorkflowManager:
  """
  WorkflowManager will be used by platform to load workflow files
  This class hold all workflows
  """
  def __init__(self):
    self.workflows = []

  def load_workflow(self, _, filepath):
    log = logger.getChild('workflow_manager')
    log.setLevel(logging.DEBUG)
    wf = Workflow(filepath)
    if wf in self.workflows:
      print("File already parsed")
      return
    else:
      self.workflows.append(wf)

