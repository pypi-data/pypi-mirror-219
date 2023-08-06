"""
DataStore Service client
"""

import io
import requests
import urllib.parse

from ursactl.core.exc import UrsaNotAuthorized

from ._base import Base

UPDATE_DATASET_MUTATION = """\
mutation update_dataset($id: ID!, $description: string!) {
    updateDataset(id: $id, description: $description) {
        errors { message }
    }
}
"""

GET_DATASET_PATH_QUERY = """\
query get_dataset($id: ID!) {
    dataset(id: $id) {
        path
        project { id handleName }
    }
}
"""

GET_DATASET_QUERY = """\
query get_dataset($id: ID!) {
    dataset(id: $id) {
        id
        path
        contentType
        description
        size
        project { id }
    }
}
"""

GET_DATASET_BY_PATH_QUERY = """\
query get_dataset($projectId: String!, $path: String!) {
    project(handleName: $projectId) {
        datasets(filter: { path: { eq: $path } }, limit: 1) {
            id
            path
            contentType
            description
            size
            project { id }
        }
    }
}
"""

DELETE_DATASET_MUTATION = """\
mutation delete_dataset($id: ID!) {
    deleteDataset(id: $id) {
        errors {
            message
        }
    }
}
"""

LIST_DATASETS_FOR_PROJECT_QUERY = """\
query listDatasets($projectId: String!) {
    project(handleName: $projectId) {
        datasets(limit:100) {
            id
            path
            size
            content_type
        }
    }
}
"""


class DssClient(Base):
    @staticmethod
    def _raise_if_none(value, var_name):
        if value is None:
            raise ValueError(f"{var_name} must be provided")

    def create_dataset(self, project_uuid=None, path=None, description=None, data=None, data_type=None, reauthorize=True):
        """
        Creates a dataset, returning the uuid and id of the dataset.

        If no data is provided, the dataset is created with no attached data.
        Data can be attached later.
        """
        # we first use the graphql to create the dataset
        # then we use a PUT to upload the data
        # the Python graphql client doesn't support multi-part HTTP requests
        self._raise_if_none(project_uuid, 'project_uuid')
        self._raise_if_none(path, 'path')
        self._raise_if_none(data, 'data')
        self._raise_if_none(data_type, 'data_type')

        # first, we POST to the right URL to upload the contents of the file
        with open(data, 'rb') as file:
            contents = file.read()
        res = requests.post(
            url=f"{self.endpoint}api/dss/{project_uuid}/{path}",
            data=contents,
            headers={
                'Content-Type': data_type,
                'Authorization': f"Bearer {self.iam_client.get_token()}"
            })

        if res.status_code == 401:  # uh oh!
            if reauthorize:
                self.iam_client.clear_token()
                return self.create_dataset(
                    project_uuid=project_uuid,
                    path=path,
                    description=description,
                    data=data,
                    data_type=data_type,
                    reauthorize=False)
            raise UrsaNotAuthorized("forbidden")
        if res.status_code == 409:
            return {'accepted': False}
        if res.status_code >= 500:
            print("Unable to create dataset. Internal platform error.")
            return {'accepted': False}

        dataset_id = res.headers['x-dataset-id']
        # if successful, we get the dataset id from the response headers
        # if we have a description, we use GraphQL to set the description

        if description is not None:
            variables = {
                'id': dataset_id,
                'description': description
            }

            query_response = self.raw_query(query=UPDATE_DATASET_MUTATION, variables=variables)
            if 'errors' in query_response:
                return {'accepted': False}

        return {
            'accepted': True,
            'id': dataset_id
        }

    def get_dataset_url(self, project_uuid=None, dataset=None):
        if self.is_uuid(dataset):
            variables = {
                'id': dataset
            }
            query_response = self.raw_query(query=GET_DATASET_PATH_QUERY, variables=variables)
            if 'errors' in query_response:
                return None
            path = query_response['data']['dataset']['path']
            handle_name = query_response['data']['dataset']['project']['handleName']
            # owner_handle = query_response['data']['dataset']['project']['user']['handle']
            # project_name = query_response['data']['dataset']['project']['name']
            return f"{self.endpoint}api/dss/{urllib.parse.quote(handle_name)}/{urllib.parse.quote(path)}"
        else:
            return f"{self.endpoint}api/dss/{urllib.parse.quote(project_uuid)}/{urllib.parse.quote(dataset)}"

    def get_dataset_details(self, dataset_id, project_uuid=None):
        if self.is_uuid(dataset_id):
            variables = {
                'id': dataset_id
            }
        else:
            dataset = self.get_dataset(dataset_id, project_uuid=project_uuid)
            if dataset is None:
                return None
            variables = {
                'id': dataset['id']
            }
        query_response = self.raw_query(query=GET_DATASET_QUERY, variables=variables)
        if 'errors' in query_response:
            return None
        return query_response['data']['dataset']

    def get_dataset(self, dataset_id, project_uuid=None):
        if self.is_uuid(dataset_id):
            variables = {
                'id': dataset_id
            }
            query_response = self.raw_query(query=GET_DATASET_QUERY, variables=variables)
            return query_response['data']['dataset']
        else:
            variables = {
                'projectId': project_uuid,
                'path': dataset_id
            }
            query_response = self.raw_query(query=GET_DATASET_BY_PATH_QUERY, variables=variables)
            return query_response['data']['project']['datasets'][0]

    def download_dataset(self, url, local_path, reauthorize=True):
        with open(local_path, 'wb') as fd:
            r = requests.get(url, stream=True, headers={
                    "authorization": f"Bearer {self.iam_client.get_token()}"
                })
            if r.status_code >= 400:
                if reauthorize:
                    self.iam_client.clear_token()
                    return self.download_dataset(url, local_path, reauthorize=False)
                return False
            for chunk in r.iter_content(chunk_size=1024*1024):
                fd.write(chunk)
        return True

    def download_dataset_content(self, url, reauthorize=True):
        local = io.StringIO()
        r = requests.get(url, stream=True, headers={
                "authorization": f"Bearer {self.iam_client.get_token()}"
            })
        if r.status_code >= 400:
            if reauthorize:
                self.iam_client.clear_token()
                return self.download_dataset_content(url, reauthorize=False)
            return False
        for chunk in r.iter_content(chunk_size=1024*1024):
            local.write(chunk)
        content = local.getvalue()
        local.close()
        return content

    def delete_dataset(self, dataset_id, project_uuid=None):
        if self.is_uuid(dataset_id):
            variables = {
                'id': dataset_id
            }
        else:
            dataset = self.get_dataset(dataset_id, project_uuid=project_uuid)
            if dataset is None:
                return False
            variables = {
                'id': dataset['id']
            }
        query_response = self.raw_query(query=DELETE_DATASET_MUTATION, variables=variables)
        if 'errors' in query_response and query_response['errors']:
            return False
        return True

    def list_datasets(self, project_scope=None):
        if project_scope is None:
            raise ValueError("project_scope must be provided")
        variables = {}
        query = LIST_DATASETS_FOR_PROJECT_QUERY
        variables = {
            'projectId': project_scope
        }
        query_response = self.raw_query(query=query, variables=variables)

        if 'errors' in query_response:
            return []
        return query_response['data']['project']['datasets']
