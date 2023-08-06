from ursactl.core.services import client
from ursactl.core._base import Base


class Project(Base):
    """
    Provides access to a project and its related resources.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._uuid is None:
            self._uuid = self.app.config.get('ursactl', 'project')

    @property
    def client(self):
        if self._client is None:
            self._client = client('usage', self.app)
        return self._client

    @property
    def name(self):
        return self._data['name']

    @property
    def description(self):
        return self._data['description']

    @property
    def is_archived(self):
        return self._data['isArchived']

    def Agent(self, *args, **kwargs):
        from ursactl.core.agent import Agent as AgentClass

        return AgentClass(*args, project_uuid=self.uuid, **kwargs)

    def agents(self):
        """
        Returns a generator listing all agents belonging to the project.
        """
        from ursactl.core.agent import Agent

        if self.uuid is None:
            return []
        planning_client = client('planning', self.app)
        return (
            Agent(client=planning_client, app=self.app, project_uuid=self.uuid, **info)
            for info in planning_client.list_agents(project_scope=self.uuid)
        )

    def agent(self, name):
        """
        Returns an agent with the given name.
        """
        planning_client = client('planning', self.app)
        info = planning_client.get_agent(name, project_uuid=self.uuid)
        return self.Agent(uuid=info['id'], client=planning_client, app=self.app, **info)

    def Dataset(self, *args, **kwargs):
        from ursactl.core.dataset import Dataset as DatasetClass

        return DatasetClass(*args, project_uuid=self.uuid, **kwargs)

    def datasets(self):
        """
        Returns a generator listing all datasets belonging to the project.
        """
        from ursactl.core.dataset import Dataset

        if self.uuid is None:
            return []
        dss_client = client('dss', self.app)
        return (
            Dataset(client=dss_client, app=self.app, project_uuid=self.uuid, **info)
            for info in dss_client.list_datasets(project_scope=self.uuid)
        )

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'name': None,
                    'description': None,
                    'isArchived': None
                }
            else:
                self._cached_data = self.client.get_project_details(self.uuid)
        return self._cached_data
