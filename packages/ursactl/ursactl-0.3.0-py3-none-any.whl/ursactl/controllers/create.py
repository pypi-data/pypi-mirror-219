import sys

from cement import Controller, ex
import json
import yaml

from ..core.services import client
from ..core.utils.magic import magic
from ursactl.controllers.utils.transforms import load_transform


def _yaml_load(fd):
    return list(yaml.load_all(fd, Loader=yaml.Loader))


class Create(Controller):
    """
    Provides the 'create' verb.
    """

    class Meta:
        label = 'create'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'create something'

    @ex(help='create agent',
        arguments=[
            (['file'], {'help': 'agent definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def agent(self):
        project_uuid = self._project_scope
        planning_client = client('planning', self.app)

        file = self.app.pargs.file
        if file.endswith('.yaml') or file.endswith('.yml'):
            loader = _yaml_load
        elif file.endswith('.json'):
            loader = json.load
        else:
            print("Only YAML and JSON files may be uploaded.")
            sys.exit(1)

        with open(file, 'r', encoding='utf-8') as fd:
            documents = loader(fd)

        if not isinstance(documents, list):
            documents = [documents]

        for content in documents:
            args = {
                'name': content['name'],
                'packages': content['packages'],
                'behaviors': content['behaviors'],
                'project_uuid': project_uuid,
            }

            result = planning_client.create_agent(**args)
            self._print(result)

    @ex(help='create transform',
        arguments=[
            (['file'], {'help': 'transform definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def transform(self):
        project_uuid = self._project_scope
        ape_client = client('ape', self.app)

        file = self.app.pargs.file
        documents = load_transform(file)

        if documents is None:
            print(f"Unable to load transform from {file}")
            sys.exit(1)

        if not isinstance(documents, list):
            documents = [documents]

        for content in documents:
            args = {
                'path': content['path'],
                'name': content['name'],
                'type': content['type'],
                'implementation': content['implementation'],
                'configuration_schema': content['configurationSchema'],
                'project_uuid': project_uuid,
            }
            if 'outputs' in content:
                args['outputs'] = content['outputs']
            if 'inputs' in content:
                args['inputs'] = content['inputs']
            if 'description' in content:
                args['description'] = content['description']

            result = ape_client.create_transform(**args)
            self._print(result)

    @ex(help='create dataset',
        arguments=[
            (['source'], {'help': 'dataset to upload', 'action': 'store'}),
            (['path'], {'help': 'path of the dataset', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['--type'], {'help': 'file type if pushing to the datastore', 'action': 'store', 'dest': 'file_type'})
         ])
    def dataset(self):
        project_uuid = self._project_scope
        path = self.app.pargs.path
        source = self.app.pargs.source
        dss_client = client('dss', self.app)
        file_type = self.app.pargs.file_type or magic(source)
        result = dss_client.create_dataset(project_uuid=project_uuid, path=path, data=source, data_type=file_type)
        self._print(result)

    @ex(help='create a new package from a file',
        arguments=[
            (['file'], {'help': 'package definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def package(self):
        project_uuid = self._project_scope
        planning_client = client('planning', self.app)

        file = self.app.pargs.file
        with open(file) as fd:
            # read the content of the file
            content = fd.read()

        result = planning_client.create_package(project_uuid=project_uuid, content=content)
        self._print(result)

    @ex(help='create a new project',
        arguments=[
            (['name'], {'help': 'project name', 'action': 'store'}),
            (['description'], {
                'help': 'project description', 'action': 'store'})
        ]
        )
    def project(self):
        projects_client = client('projects', self.app)
        result = projects_client.create(
            name=self.app.pargs.name, description=self.app.pargs.description)
        self._print(result)

    @ex(help='create a generator from a file',
        arguments=[
            (['file'], {'help': 'generator definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def generator(self):
        ape_client = client('ape', self.app)

        file = self.app.pargs.file
        if file.endswith('.yaml') or file.endswith('.yml'):
            loader = _yaml_load
        elif file.endswith('.json'):
            loader = json.load
        else:
            print("Only YAML and JSON files may be uploaded.")
            sys.exit(1)

        with open(file, 'r', encoding='utf-8') as fd:
            documents = loader(fd)

        if not isinstance(documents, list):
            documents = [documents]

        for content in documents:
            args = {
                'path': content['path'],
                'transform': content['transform']['path'],
                'transform_configuration': content['transform']['configuration'],
                'load': content['load'],
                'project_uuid': self._project_scope
            }

            for key in ['extract', 'description']:
                if key in content and content[key] is not None:
                    args[key] = content[key]

            result = ape_client.create_generator(**args)
            self._print(result)

    @ex(help='create a pipeline from a file',
        arguments=[
            (['file'], {'help': 'pipeline definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def pipeline(self):
        ape_client = client('ape', self.app)

        file = self.app.pargs.file
        if file.endswith('.yaml') or file.endswith('.yml'):
            loader = _yaml_load
        elif file.endswith('.json'):
            loader = json.load
        else:
            print("Only YAML and JSON files may be uploaded.")
            sys.exit(1)

        with open(file, 'r', encoding='utf-8') as fd:
            documents = loader(fd)

        if not isinstance(documents, list):
            documents = [documents]

        for content in documents:
            args = {
                'path': content['path'],
                'project_uuid': self._project_scope
            }

            for key in ['seeders', 'generators', 'description']:
                if key in content and content[key] is not None:
                    args[key] = content[key]

            result = ape_client.create_pipeline(**args)
            self._print(result)

    def _print(self, data):
        if self.app.pargs.output == 'json':
            print(json.dumps(data))
        else:
            print(yaml.dump(data))

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get('ursactl', 'project')
