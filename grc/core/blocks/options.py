from . import Block, register_build_in
from ._templates import MakoTemplates
from ._build import build_params
from ..base import Element
from ..params import Param

from collections import OrderedDict, defaultdict
import typing

templates = MakoTemplates()

@register_build_in
class Options(Block):
    """
    Implementation of Options block for codegen purpose
    This block will be used to select workflow and provide informations for code generator
    """
    key = 'options' # block id
    label = 'Options' # block name

    cpp_templates = MakoTemplates()
    file_format = 1

    def __init__(self, parent):
        self.raw_params_data = [
            dict(id='title',
                label='Title',
                workflow='',
                dtype='string',
                default='',
                hide="${ ('none' if title else 'part') }",
            ),
            dict(id='author',
                label='Author',
                workflow='',
                dtype='string',
                default='',
                hide="${ ('none' if author else 'part') }",
            ),
            dict(id='copyright',
                label='Copyright',
                workflow='',
                dtype='string',
                default='',
                hide="${ ('none' if copyright else 'part') }",
            ),
            dict(id='description',
                label='description',
                workflow='',
                dtype='string',
                default='',
                hide="${ ('none' if description else 'part') }",
            ),
            dict(id='output_language',
                label='Output Language',
                workflow='',
                dtype='enum',
                default='python',
                options=['python'],
                option_labels=['Python'],
                hide="none",
            ),
            dict(id='generate_options',
                label='Generate Options',
                workflow='',
                dtype='enum',
                default='qt_gui',
                options=['qt_gui'],
                option_labels=['QT GUI'],
                hide="none",
            ),
            dict(id='gen_linking',
                label='Linking',
                workflow='',
                dtype='enum',
                default='dynamic',
                options=['dynamic', 'static'],
                option_labels=['dynamic', 'static'],
                hide="all",
            ),
            dict(id='thread_safe_setters',
                label='Thread-safe setters',
                workflow='',
                category='Advanced',
                dtype='enum',
                options=['', '1'],
                option_labels=['Off', 'On'],
                hide="part",
            ),
            dict(id='catch_exceptions',
                label='Catch Block Exceptions',
                workflow='',
                category='Advanced',
                dtype='enum',
                default='True',
                options=['False', 'True'],
                option_labels=['Off', 'On'],
                hide="part",
            ),
            dict(id='hier_block_src_path',
                label='Hier Block Source Path',
                workflow='',
                category='Advanced',
                dtype='string',
                options='.:',
                hide="part",
            ),
            dict(id='generator_class_name',
                workflow='',
                dtype='string',
                hide="all",
            ),
            dict(id='generator_module',
                workflow='',
                dtype='string',
                hide="all",
            ),
        ]

        self.default_ids = [
            'title',
            'author',
            'copyright',
            'description',
            'output_language',
            'generate_options',
            'gen_linking',
            'thread_safe_setters',
            'catch_exceptions',
            'hier_block_src_path',
        ]

        self.parent_platform = parent.parent_platform
        self.workflows = self.parent_platform.workflow_manager.workflows # get all available workflow objects
        self.codegen_options = dict() # key: output_language, val: list of generator_options
        self.current_workflow = None
        self.workflow_params = []

        self.parse_workflows()

        # construct output_language parameter
        temp_dct = dict(
            id='output_language',
            label='Output Language',
            dtype='enum',
            options=[],
            option_labels=[],
        )

        for output_language, output_language_label in self.codegen_options.keys():
            temp_dct['options'].append(output_language)
            temp_dct['option_labels'].append(output_language_label)

        self.raw_params_data[4] = temp_dct
        self.parameters_data = build_params(
            params_raw=self.raw_params_data,
            have_inputs=False,
            have_outputs=False,
            flags=Block.flags,
            block_id=self.key,
        )

        super().__init__(parent)

    def insert_grc_parameters(self, grc_parameters):
        """
        Update parameters with values from the grc file
        Args:
            grc_parameters (str): option block parameter values from grc
        """
        self.params['output_language'].value = grc_parameters.get('output_language')
        self.params['generate_options'].value = grc_parameters.get('generate_options')
        self.update_current_workflow()

        for i in range(len(self.workflow_params)):
            self.workflow_params[i]['params']['id'].value = grc_parameters.get('id')
            for default_id in self.default_ids:
                if default_id == 'output_language' or default_id == 'generate_options':
                    continue
                self.workflow_params[i]['params'][default_id].value = grc_parameters.get(default_id)

        self.params = self.get_params_by_workflow_id(self.current_workflow.id)
        self.parent.validate() # validiate the flow graph

    def rewrite(self) -> None:
        """        
        Update generated_options each time the value of output_language is changed
        Update category parameter
        """
        self.update_current_workflow()
        latest_outlang = self.params['output_language'].value
        latest_genopt = self.params['generate_options'].value
        self.params = self.get_params_by_workflow_id(self.current_workflow.id)

        self.params['output_language'].value = latest_outlang
        self.params['generate_options'].value = latest_genopt

        choosen_language = self.params['output_language'].value
        output_language_pair = ()
        for output_language, output_language_label in self.codegen_options.keys():
            if choosen_language == output_language:
                output_language_pair = (output_language, output_language_label)
                break

        list_of_generated_options_pair = self.codegen_options[output_language_pair]

        tmp_dct = OrderedDict()
        tmp_dct.attributes = defaultdict(dict)
        for generated_options, generated_options_label in list_of_generated_options_pair:
            tmp_dct[generated_options] = generated_options_label
        self.params['generate_options'].options = tmp_dct

        self.update_generator_class()
        Element.rewrite(self)
        super().rewrite()
        return

    def get_params_by_workflow_id(self, id) -> OrderedDict[str, Param]:
        for wf in self.workflow_params:
            if wf['workflow_id'] == id:
                return wf['params']

    def parse_workflows(self) -> None:
        """
        Read all workflow yml file
        for each workflow, use pair for output_language, generator_options and their label
        then, put it on codegen_options

        also insert parameters from workflow files into self.workflow_params

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

        for workflow in self.workflows:
            tmp = dict()
            tmp['workflow_id'] = workflow.id
            from copy import deepcopy
            arr = deepcopy(self.raw_params_data)

            tmp['params'] = self.new_params_from_list(arr + workflow.parameters)
            tmp['params']['output_language'].set_value(workflow.output_language)
            tmp['params']['generate_options'].set_value(workflow.generator_options)

            tmp_dct = OrderedDict()
            tmp_dct.attributes = defaultdict(dict)
            for output_language, output_language_label in self.codegen_options.keys():
                tmp_dct[output_language] = output_language_label
            tmp['params']['output_language'].options = tmp_dct

            choosen_language = workflow.output_language
            output_language_pair = ()
            for output_language, output_language_label in self.codegen_options.keys():
                if choosen_language == output_language or choosen_language == output_language_label:
                    output_language_pair = (output_language, output_language_label)
                    break

            list_of_generated_options_pair = self.codegen_options[output_language_pair]

            tmp_dct = OrderedDict()
            tmp_dct.attributes = defaultdict(dict)
            for generated_options, generated_options_label in list_of_generated_options_pair:
                tmp_dct[generated_options] = generated_options_label
            tmp['params']['generate_options'].options = tmp_dct

            self.workflow_params.append(tmp)

    def new_params_from_list(self, lst) -> OrderedDict[str, Param]:
        param_factory = self.parent_platform.make_param
        new_params_data = build_params(
            params_raw=lst.copy(),
            have_inputs=False,
            have_outputs=False,
            flags=Block.flags,
            block_id=self.key
        )
        new_params: typing.OrderedDict[str, Param] = (OrderedDict(
            (data['id'], param_factory(parent=self, **data)) for data in new_params_data))
        return new_params

    def update_current_workflow(self) -> None:
        """
        get current workflow based on the current value of output language and generate options
        """
        for workflow in self.workflows:
            if workflow.output_language == self.params['output_language'].get_value() \
                and workflow.generator_options == self.params['generate_options'].get_value():
                self.current_workflow = workflow
                return

    def update_generator_class(self) -> None:
        """
        Update the generator_class_name and generator_module parameters based on the current output language
        """
        self.params['generator_class_name'].set_value(self.current_workflow.generator_class)
        self.params['generator_module'].set_value(self.current_workflow.generator_module)
