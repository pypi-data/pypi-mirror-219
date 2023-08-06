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
from unify.helpers.graph_ql.permissions import PermissionsGraphQl
from unify.helpers.Permissions import DisplayNames


class Permissions(ApiRequestManager):
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

        self.query_builder = PermissionsGraphQl()

    def get_org_config(self, org_id):
        """
        Retrieves the organization permissions configuration

        :param org_id: Organization ID to be queried
        :return:
        """
        resp = self.graph_ql_query(
            org_id=org_id,
            query=self.query_builder.get_org_config()
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def get_rules(self, org_id):
        """
        Retrieves the organization id applied rules

        :param org_id: Organization ID to be queried
        :return:
        """
        resp = self.graph_ql_query(
            org_id=org_id,
            query=self.query_builder.get_rules()
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def get_user_rules(self, org_id, user_id):
        """
        Retrieves the applied rules to a given user

        :param org_id: Organization id where the user is stored
        :param user_id: User ID to be queried
        :return:
        """

        resp = self.graph_ql_query(
            org_id=org_id,
            query=self.query_builder.get_user_rules(user_id=user_id)
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def get_artifact_rules(self, org_id, artifact_id, artifact_type):
        """
        Retrieves the applied rules to a given artifact

        :param org_id: Organization id where the artifact is stored
        :param artifact_id: Artifact Identification UUID
        :param artifact_type: Dataset or Pipeline
        :return:
        """
        query = self.query_builder.get_artifact_rules(
            artifact_id=artifact_id,
            artifact_type=artifact_type
        )

        resp = self.graph_ql_query(
            org_id=org_id,
            query=query
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def get_selector_definitions(self, org_id):
        """
        Retrieve selector definitions of a given org

        :param org_id: Organization ID
        :return:
        """
        resp = self.graph_ql_query(
            org_id=org_id,
            query=self.query_builder.get_selector_definitions()
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def check_permission(self, org_id, artifact_type, artifact_id, user_id, verb):
        """
        Checks the permissions applied to a given artifact and user

        :param org_id: Organization identification where the artifact and user are stored
        :param artifact_type: Dataset or Pipeline
        :param artifact_id: Artifact Identification UUID
        :param user_id: User identification UUID
        :param verb:
        :return:
        """
        query = self.query_builder.check(
            artifact_type=artifact_type,
            artifact_id=artifact_id,
            user_id=user_id,
            verb=verb
        )

        resp = self.graph_ql_query(
            org_id=org_id,
            query=query
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def get_selector_definition(self, org_id, selector_id):
        """
        Retrieve the selector definition

        :param org_id:  Organization identification where the selector is stored
        :param selector_id: Selector ID to query
        :return:
        """

        resp = self.graph_ql_query(
            org_id=org_id,
            query=self.query_builder.get_selector_definition(selector_id=selector_id)
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def add_rule(self, org_id, domain, verb, effect, userSelector, resourceSelector):
        """
        Adds a new permission rule

        :param org_id:  Organization identification where the selector is stored
        :param domain: unify.helpers.Permissions.Domains
        :param verb: unify.helpers.Permissions.Verbs
        :param effect: unify.helpers.Permissions.Effects
        :param userSelector: unify.helpers.Permissions.SelectorBool
        :param resourceSelector: unify.helpers.Permissions.SelectorBool
        :return:
        """

        query = self.query_builder.build_rule_mutation(
            domain=domain,
            verb=verb,
            effect=effect,
            userSelector=userSelector,
            resourceSelector=resourceSelector
        )

        resp = self.graph_ql_query(
            org_id=org_id,
            query=query
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))

    def get_specific_selectors(self, org_id, user: bool, display_name: str = None):
        """
        Retrieve a given selector

        :param org_id: Organization identification where the selector is stored
        :param user: User identification UUID
        :param display_name: The selector name
        :return:
        """
        selectors = self.get_selector_definitions(org_id=org_id)

        selector_type = "user" if user else "resource"

        selected = []

        if "data" in selectors:

            data = selectors["data"]

            if "permissions" in data:

                per = data["permissions"]

                if "getSelectorDefinitions" in per:

                    for selector in per["getSelectorDefinitions"]:

                        if selector["selectorType"] == selector_type:
                            if display_name:
                                if selector["displayName"] == display_name:
                                    selected.append(selector["id"])
                            else:
                                selected.append(selector["id"])

        return selected

    def get_everyone_user_selectors(self, org_id):
        return self.get_specific_selectors(org_id=org_id, user=True, display_name=DisplayNames.everyone)

    def get_nobody_user_selectors(self, org_id):
        return self.get_specific_selectors(org_id=org_id, user=True, display_name=DisplayNames.nobody)

    def get_everything_resource_selectors(self, org_id):
        return self.get_specific_selectors(org_id=org_id, user=False, display_name=DisplayNames.everything)

    def get_nothing_resource_selectors(self, org_id):
        return self.get_specific_selectors(org_id=org_id, user=False, display_name=DisplayNames.nothing)

    def delete_rule(self, org_id, rule_id):
        resp = self.graph_ql_query(
            org_id=org_id,
            query=self.query_builder.build_delete_rule_mutation(
                rule_id=rule_id
            )
        )

        if resp.status_code in self.OK:
            return json.loads(resp.content)

        raise Exception(repr(resp.content))
