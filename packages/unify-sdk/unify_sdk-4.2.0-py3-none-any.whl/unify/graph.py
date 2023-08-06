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
Contains methods to interact with graphs api
"""
import json
import io

import json_lines

from unify.properties import Properties
from unify.properties import ClusterSetting
from unify.apirequestsmng import ApiRequestManager
from unify.helpers.SingleOrg import single_org


class Graph(ApiRequestManager):
    """
    Class to interact with pipeline endpoints
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

        self.graph_url = remote + 'graph/v1'

        self.graph_query_url = self.graph_url + "/{}/query"

        self.export_query_url = self.graph_query_url + "/export"

        self.graph_merge_url = self.graph_url + "/merge"

        #https://aws-stage-qa-1.ean.io/graph/v1/merge?name=Try+building+a+new+graph

    @single_org
    def get_graphs_list(self, org_id=None):
        """
        Retrieves the list of graphs on the given org

        :param org_id: organization Id to be queried
        :return: Array containing list of graphs data
        """

        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        result = self.session.get(self.graph_url, headers=header)

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def query_graph(self, org_id=None, *, graph, query, json_format=False):
        """
        Runs a cypher query on the given graph

        :param org_id: Organization id where the graph is stored
        :param graph: Graph id to be queried
        :param query: Cypher query
        :param json_format: return the results in a universal correctly json o json lines
        :return:
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_octet
        )

        final_url = self.graph_query_url.format(graph)

        result = self.session.post(final_url, headers=header, data=query)

        if result.status_code in [200, 201, 202]:
            iobytes = io.BytesIO(result.content)
            full_graph = []
            if json_format:
                for item in json_lines.reader(iobytes):
                    full_graph.append(item)

                return full_graph

            return result.content

        raise Exception(repr(result.content))

    @single_org
    def export_query(self, org_id=None, *, graph, query, nodes_dataset_name, edges_dataset_name):
        """
        Export a given cypher query into 2 datasets

        :param org_id: Organization id where the graph is stored
        :param graph: Graph id to be queried
        :param query: Cypher query
        :return:
        """

        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_octet
        )

        final_url = self.export_query_url.format(graph)

        data = (["nodesDatasetName", nodes_dataset_name], ["edgesDatasetName", edges_dataset_name])

        result = self.session.post(final_url, headers=header, data=query, params=data)

        if result.status_code in [200, 201, 202]:
            return result.content

        raise Exception(json.loads(result.content))

    @single_org
    def create_empty_graph(self, org_id=None, *, graph_name):
        """
        Create an empty graph with the given name

        :param org_id: Organization id where the graph would be stored
        :param graph_name: Empty graph name
        :return:
        """

        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        data = {"name": graph_name}

        result = self.session.post(self.graph_merge_url, headers=header, params=data)

        if result.status_code in [200, 201, 202]:
            return json.loads(result.content)

        raise Exception(json.loads(result.content))
