# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Contains methods to interact with connector service
"""
import json
from enum import Enum
from datetime import datetime

from unify.properties import Properties
from unify.properties import ClusterSetting
from unify.apirequestsmng import ApiRequestManager
from unify.helpers.SingleOrg import single_org

class ConnStatus(str, Enum):
    """
    Connector status
    """
    ERROR = 'error'
    GOOD = 'good'
    UNKNOWN = 'unknown'

class LogType(str, Enum):
    """
    Log message severity
    """
    ERROR = 'error'
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'

class ArtifactType(str, Enum):
    """
    Artifact type
    """
    CONNECTOR = 'connector'
    DATASET = 'dataset'
    GRAPH = 'graph'
    PIPELINE = 'pipeline'
    TEMPLATE = 'template'


class Connectors(ApiRequestManager):
    """
    Class to interact with connectors endpoints
    """

    def __init__(self, cluster=None, props=Properties(ClusterSetting.KEY_RING), org_id=None):

        """
        Class constructor

        :param cluster: Cluster name to be used
        :type cluster: str
        :param props: Properties instantiated object
        :type props: class:`unify.properties.Properties`
        """
        super().__init__(cluster=cluster, props=props, org_id=org_id)

        remote = self.props.get_remote(self.cluster)

        self.connectors_url = remote + 'connectors/'
        self.update_status_url = self.connectors_url + "{}/updateStatus"
        self.update_config_url = self.connectors_url + "{}/updateConfig"
        self.get_connector_url = self.connectors_url + "{}"
        self.write_log_url = self.connectors_url + "{}/writeLog"
        self.get_artifacts_url = self.connectors_url + "{}/artifacts"
        self.healthcheck_url = self.connectors_url + "healthcheck"
        self.create_with_user_url = self.connectors_url + "create-with-user"

    @single_org
    def create_connector(self, org_id=None, *, name, connector_type, config):
        """
        Create a new connector

        :param org_id: organization Id to be queried
        :param name: connector name
        :param connector_type: type of the connector
        :param config: connector config
        :return: connector id
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        body = {
            'name': name,
            'type': connector_type,
            'config': config,
        }

        result = self.session.post(self.connectors_url, headers=header, json=body)

        if result.status_code in self.OK:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def update_connector_status(self, org_id=None, *, connector_id, status, metadata=''):
        """
        Updates connector status

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be updated
        :param status: new status to update
        :param metadata: connector metadata to be updated
        :return: API response
        """

        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        body = {
            'status': status,
            'metadata': metadata
        }

        result = self.session.put(
            self.update_status_url.format(connector_id),
            headers=header,
            json=body
        )

        if result.status_code in self.OK:
            return True

        raise Exception(repr(result.content))

    @single_org
    def update_connector_config(self, org_id=None, *, connector_id, config):
        """
        Update connector configuration

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be updated
        :param config: Config to be updated
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )
        result =  self.session.put(
            self.update_config_url.format(connector_id),
            headers=header,
            json=config
        )

        if result.status_code in self.OK:
            return True

        raise Exception(repr(result.content))

    @single_org
    def get_connector(self, org_id=None, *, connector_id):
        """
        Returns the description of a given connector. Will be called periodically by the connector
        to get updated configuration

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be returned
        :return: Connector info
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )
        result = self.session.get(self.get_connector_url.format(connector_id), headers=header)

        if result.status_code in self.OK:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def delete_connector(self, org_id=None, *, connector_id):
        """
        Delete connector

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be returned
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )
        result = self.session.delete(self.get_connector_url.format(connector_id), headers=header)

        if result.status_code in self.OK:
            return True

        raise Exception(repr(result.content))

    @single_org
    def write_log(
        self,
        org_id=None,
        *,
        connector_id,
        message,
        timestamp=None,
        log_type=LogType.INFO,
        metadata=''
    ):
        """
        Add a log entry

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be returned
        :param message: log message
        :param timestamp: timestamp of the log message
        :param type: severity of the log
        :param metadata: log message metadata
        """
        if timestamp is None:
            timestamp = int(datetime.now().timestamp() * 1000)

        body = [{
            "timestamp": timestamp,
            "type": log_type,
            "message": message,
            "metadata": metadata
        }]

        self.write_logs(org_id, connector_id=connector_id, log_list=body)

    @single_org
    def write_logs(self, org_id=None, *, connector_id, log_list):
        """
        Add a list of log entries

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be returned
        :param log_list: log messages in list of dicts with keys: "timestamp", "type", "message",
        "metadata"
        """

        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )

        result = self.session.post(
            self.write_log_url.format(connector_id),
            headers=header,
            json=log_list
        )

        if result.status_code in self.OK:
            return True

        raise Exception(repr(result.content))

    @single_org
    def get_artifacts(self, org_id=None, *, connector_id):
        """
        Get registered artifacts

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be returned
        :return: List of artifacts linked
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )
        result = self.session.get(self.get_artifacts_url.format(connector_id), headers=header)

        if result.status_code in self.OK:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def create_artifacts(self, org_id=None, *, connector_id, artifacts_list):
        """
        Register artifacts

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be returned
        :param artifacts_list: artifacts info into list of dicts with keys: "artifactType",
        "artifactId", "artifactName"
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )
        result = self.session.post(
            self.get_artifacts_url.format(connector_id),
            headers=header,
            json=artifacts_list
        )
        if result.status_code in self.OK:
            return True

        raise Exception(repr(result.content))

    @single_org
    def create_artifact(
        self,
        org_id=None,
        *,
        connector_id,
        artifact_type,
        artifact_id,
        artifact_name
    ):
        """
        Register a single artifact

        :param org_id: organization Id to be queried
        :param connector_id: Connector id to be returned
        :param artifacts_list: artifacts info into list of dicts with keys: "artifactType",
        "artifactId", "artifactName"
        """
        body = [{
            "artifactType": artifact_type,
            "artifactId": artifact_id,
            "artifactName": artifact_name
        }]
        return self.create_artifacts(org_id, connector_id=connector_id, artifacts_list=body)

    def healthcheck(self, encoding='utf8'):
        """
        Returns the health status of the connector service
        """
        result = self.session.get(self.healthcheck_url)
        if result.status_code in self.OK:
            return result.content.decode(encoding)

        raise Exception(repr(result.content))

    @single_org
    def create_connector_with_user(self, org_id=None, *, name, connector_type, config):
        """
        Create a new connector, creating an associated user as well

        :param org_id: organization Id to be queried
        :param name: connector name
        :param connector_type: type of the connector
        :param config: connector config
        :return: connector id and user info
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )

        body = {
            'name': name,
            'type': connector_type,
            'config': config,
        }
        result = self.session.post(self.create_with_user_url, headers=header, json=body)
        if result.status_code in self.OK:
            return json.loads(result.content)

        raise Exception(repr(result.content))
