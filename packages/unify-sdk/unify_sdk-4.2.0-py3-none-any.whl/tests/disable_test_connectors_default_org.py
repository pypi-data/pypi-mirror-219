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

import unittest
from tests import *
from unify.connectors import ConnStatus, ArtifactType

class TestSourcesWithOrgID(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connectors = Connectors(cluster=cluster_name, props=props, org_id=test_org)

    @unittest.skip('Connector service is broken')
    def test_creation_delete_connector(self):
        conn_id = self.connectors.create_connector(
            name='wmorales_test',
            connector_type='wmorales_type',
            config={'a':'b','c':'d'}
        )
        self.connectors.get_connector(connector_id=conn_id)
        self.connectors.delete_connector(connector_id=conn_id)
        try:
            self.connectors.get_connector(connector_id=conn_id)
            raise Exception('Connector is not deleted')
        except Exception as err:
            self.assertTrue(
                (err.args[0] == "b'The requested resource could not be found.'") or
                (err.args[0] == "b'java.util.NoSuchElementException: Invoker.first'")
            )

    @unittest.skip('Connector service is broken')
    def test_get_connector(self):
        connector = self.connectors.get_connector(connector_id=test_connector)
        result = {}
        result['id'] = connector['id']
        result['type'] = connector['type']
        self.assertEqual(result, {'id':test_connector, 'type':'connector_test_type'})

    @unittest.skip('Connector service is broken')
    def test_update_connector_status(self):
        self.connectors.update_connector_status(
            connector_id=test_connector,
            status=ConnStatus.ERROR,
        )
        connector = self.connectors.get_connector(connector_id=test_connector)
        self.assertEqual(connector['status'], 'error')

    @unittest.skip('Connector service is broken')
    def test_update_connector_config(self):
        self.connectors.update_connector_config(
            connector_id=test_connector,
            config={'a':'b','c':'d'}
        )
        connector = self.connectors.get_connector(connector_id=test_connector)
        self.assertEqual(connector['config'], {'a':'b','c':'d'})

    # TODO Run test again when endpoint is fixed
    @unittest.skip('Write logs endpoint needs to be fixed in prod')
    def test_write_log(self):
        self.connectors.write_log(
            connector_id=test_connector,
            message='Python SDK connectors test'
        )
        self.assertTrue(True)

    @unittest.skip('Connector service is broken')
    def test_create_get_artifact(self):
        self.connectors.create_artifact(
            connector_id=test_connector,
            artifact_type=ArtifactType.TEMPLATE,
            artifact_id='67890',
            artifact_name="Python_SDK_connectors_artifact_test_default_org"
        )
        artifact = self.connectors.get_artifacts(connector_id=test_connector)
        self.assertTrue({
            'artifactType': 'template',
            'artifactId': '67890',
            'artifactName': 'Python_SDK_connectors_artifact_test_default_org'
        } in artifact)

    @unittest.skip('Connector service is broken')
    def test_helthcheck(self):
        self.assertEqual(self.connectors.healthcheck(), 'Healthy')
