import logging
import yaml

# todo 

logger = logging.getLogger(__name__)

class Workflow:
    """
    Workflow class is used to parse workflow file

    Attributes:
        id (str): unique name of workflow
        descripton (str): detailed information of workflow
        output_language (str): target language
        output_language_label (str): Information for users about the target language of the workflow
        generator_class (str): Name of the code generator class
        generator_module (str): Module name of where the code generator class is located
        generator_options (str): Used to select a workflow
        generator_options_label (str): Information for users to select a workflow
        parameters (arr of dict): parameters for options block
        asserts (arr): array of assert statements
        context (dict): additional workflow parameters
    """
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            with open(args[0], 'r') as wf:
                self.workflow_params = yaml.safe_load(wf)
        else:
            self.workflow_params = kwargs

        self.id = self.workflow_params.pop('id')
        self.descripion = self.workflow_params.pop('description')
        self.output_language = self.workflow_params.pop('output_language')
        self.output_language_label = self.workflow_params.pop('output_language_label')
        self.generator_class = self.workflow_params.pop('generator_class')
        self.generator_module = self.workflow_params.pop('generator_module')
        self.generator_options = self.workflow_params.pop('generator_options')
        self.generator_options_label = self.workflow_params.pop('generator_options_label')
        self.parameters = self.workflow_params.pop('parameters', [])
        self.templates = self.workflow_params.pop('templates', {})
        self.cpp_templates = self.workflow_params.pop('cpp_templates', {})
        self.asserts = self.workflow_params.pop('asserts', [])
        self.context = self.workflow_params # additional workflow parameters


class WorkflowManager:
    """
    WorkflowManager will be used by platform to load workflow files
    This class hold all workflows

    Attributes:
        workflows: all available workflow objects
    """
    def __init__(self):
        self.workflows = []

    def load_workflow(self, _, filepath) -> None:
        """
        This function will be called by platform on app initialization
        to load all availble workflows
        Args:
        _ (any): Unused
        filepath (str): path of workflow file
        """
        log = logger.getChild('workflow_manager')
        log.setLevel(logging.DEBUG)
        wf = Workflow(filepath)
        if wf not in self.workflows:
            self.workflows.append(wf)

