from pathlib import Path
import sys

from cement import Controller
import json
import yaml

from ..core.services import client
import ursactl.controllers.utils.transforms


class Sync(Controller):
    """
    Provides the 'sync' verb
    """

    class Meta:
        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'synchronize a directory with Ursa Frontier'
        arguments = [
            (['--project'], {
                 'help': 'override default project to use with this repository',
                 'dest': 'project',
                 'action': 'store'}),
            (['--dir', '--directory'], {
                 'help': 'directory to initialize (defaults to \'.\')',
                 'dest': 'directory',
                 'action': 'store',
                 'default': '.'}),
        ]

    def _default(self):
        root = Path(self.app.pargs.directory)
        if not root.exists():
            print("Error: %s does not exist." % root)
            sys.exit(1)
        elif not root.is_dir():
            print("Error: %s exists and is not a directory." % root)
            sys.exit(1)
        ape_client = client('ape', self.app)

        resources = self._load_resources(root)

        # now we can sync resources
        self._sync_datasets(resources['dataset'])
        self._sync_transforms(ape_client, resources['transform'])
        self._sync_generators(ape_client, resources['generator'])
        self._sync_pipelines(ape_client, resources['pipeline'])

    def _sync_datasets(self, datasets):
        pass

    def _sync_transforms(self, client, transforms):
        for item in client.list_transforms(self._project_scope):
            if item['path'] not in transforms and item['isSynced']:
                client.delete_synced_transform(item['id'])
            elif item['path'] in transforms and not item['isSynced']:
                print(f"Unable to sync transform #{item['path']} because it is not synced.")
                transforms.delete(item['path'])
        for item in transforms.values():
            args = {
                'path': item['path'],
                'name': item['name'],
                'type': item['type'],
                'implementation': item['implementation'],
                'configuration_schema': item['configurationSchema'],
                'project_uuid': self._project_scope,
            }
            if 'outputs' in item:
                args['outputs'] = item['outputs']
            if 'inputs' in item:
                args['inputs'] = item['inputs']
            if 'description' in item:
                args['description'] = item['description']
            result = client.sync_transform(**args)
            self._print(result)

    def _sync_generators(self, client, generators):
        for item in client.list_generators(self._project_scope):
            if item['path'] not in generators and item['isSynced']:
                client.delete_synced_generator(item['id'])
            elif item['path'] in generators and not item['isSynced']:
                print(f"Unable to sync generator #{item['path']} because it is not synced.")
                generators.delete(item['path'])
        for item in generators.values():
            args = {
                'path': item['path'],
                'transform': item['transform']['path'],
                'transform_configuration': item['transform']['configuration'],
                'load': item['load'],
                'project_uuid': self._project_scope
            }

            for key in ['extract', 'description']:
                if key in item and item[key] is not None:
                    args[key] = item[key]

            result = client.sync_generator(**args)
            self._print(result)

    def _sync_pipelines(self, client, pipelines):
        for item in client.list_pipelines(self._project_scope):
            if item['path'] not in pipelines and item['isSynced']:
                client.delete_synced_pipeline(item['id'])
            elif item['path'] in pipelines and not item['isSynced']:
                print(f"Unable to sync pipeline #{item['path']} because it is not synced.")
                pipelines.delete(item['path'])
        for item in pipelines.values():
            args = {
                'path': item['path'],
                'project_uuid': self._project_scope
            }
            for key in ['seeders', 'generators', 'description']:
                if key in item and item[key] is not None:
                    args[key] = item[key]

            result = client.sync_pipeline(**args)
            self._print(result)

    def _load_resources(self, root):  # noqa: C901
        # we want to look at each resource we can find locally and compute a hash
        # that makes sense for the data stored on the server - to see if there's a difference
        # for now, we're focused on the data side of things
        # we'll need to look at the planning side of things later
        # we look in each of the directories created by `init`, but use them only to
        # establish the default resource type. Resources can have a `kind` metadata
        # attribute that we can use to determin the kind of resource we're looking at.
        # datasets are special, but the same file with the .yaml extension can house
        # the metadata (so foo.csv has a foo.csv.yaml metadata file)
        #
        # OR, for datasets, we can have an index.yaml file that lists all of the datasets
        # we want to sync along with their metadata. Or both, until we find out which one
        # users find easiest to use.
        resources = {
            'transform': {},
            'generator': {},
            'pipeline': {},
            'dataset': {},
        }

        for file in root.rglob("*"):
            if file.is_dir():
                continue
            if file.stat().st_size == 0:
                continue
            if file.name.startswith('.'):
                continue
            info = None
            suffix = file.suffix
            if suffix == '.md':
                # likely a transform
                with open(file, "r") as fd:
                    info = ursactl.controllers.utils.transforms.load_from_markdown(fd)
            if suffix == '.lua':
                # likely a transform
                with open(file, "r") as fd:
                    info = ursactl.controllers.utils.transforms.load_from_lua(fd)
            elif suffix in ['.yaml', '.yml']:
                with open(file, "r") as fd:
                    info = list(yaml.load_all(fd, Loader=yaml.Loader))
            elif suffix == '.json':
                with open(file, "r") as fd:
                    info = json.load(fd)
            else:
                continue
            info = info if isinstance(info, list) else [info]
            for item in info:
                kind = self._get_kind(root, file, item)
                if kind in resources:
                    resources[kind][item['path']] = item

        return resources

    def _get_kind(self, root, file, info) -> str:
        if 'kind' in info and info['kind'] not in (None, ''):
            return info['kind']
        if file.suffix in ['.yaml', '.yml'] and file.with_name(file.stem).exists():
            return 'dataset'
        bits = file.relative_to(root).parts
        for type in ['transforms', 'generators', 'pipelines', 'datasets']:
            if type in bits:
                return type[:-1]
        return 'unknown'

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get('ursactl', 'project')

    def _print(self, data):
        print(yaml.dump(data))
