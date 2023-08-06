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
from unify.permissions import Permissions
from unify.helpers.Permissions import ArtifactType
from unify.helpers.Permissions import Verbs, Domains, Effects, DisplayNames
import json
import os
import uuid
from tests import test_org, cluster_name, props, test_dataset


class TestTemplates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.permissions = Permissions(
            cluster=cluster_name,
            props=props
        )

    def test_get_org_config(self):

        try:
            response = self.permissions.get_org_config(org_id=test_org)

            assert True, ""
        except Exception as e:
            assert False, str(e)

    def test_get_rules(self):
        try:
            response = self.permissions.get_rules(org_id=test_org)
            assert True, ""
        except Exception as e:
            assert False, str(e)

    def test_get_user_rules(self):
        try:
            response = self.permissions.get_user_rules(org_id=test_org, user_id=1)

            assert True, ""
        except Exception as e:
            assert False, str(e)

    def test_get_dataset_rules(self):

        try:
            self.permissions.get_artifact_rules(
                org_id=test_org,
                artifact_type=ArtifactType.dataset,
                artifact_id=test_dataset["id"]
            )

            assert True, "Get datasets rule"

        except Exception as e:
            assert False, str(e)

    def test_selector_definitions(self):
        try:
            response = self.permissions.get_selector_definitions(org_id=test_org)
            assert True, ""
        except Exception as e:
            assert False, str(e)

    def test_check_permission(self):
        try:
            response = self.permissions.check_permission(
                org_id=test_org,
                artifact_type=ArtifactType.dataset,
                artifact_id=test_dataset["id"],
                verb=Verbs.write,
                user_id=1
            )
            assert True, ""
        except Exception as e:
            assert False, str(e)

    def test_get_selector_definition(self):
        try:
            response = self.permissions.get_selector_definition(
                org_id=test_org,
                selector_id=1
            )

            assert True, ""
        except Exception as e:
            assert False, str(e)

    def test_add_rule(self):
        try:
            response = self.permissions.add_rule(
                org_id=test_org,
                domain=Domains.dataset,
                effect=Effects.allow,
                verb=Verbs.write,
                userSelector=1,
                resourceSelector=3
            )

            assert True, ""
        except Exception as e:
            assert False, str(e)

    def test_get_user_specific_connector(self):
        response = self.permissions.get_specific_selectors(org_id=test_org, user=True)

        assert len(response) > 0, "No selectors found for users"

    def test_get_resource_specific_connector(self):
        response = self.permissions.get_specific_selectors(org_id=test_org, user=False)

        assert len(response) > 0, "No selectors found for resources"

    def test_get_user_all_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=True,
            display_name=DisplayNames.everyone
        )

        assert len(response) > 0, "No selectors found for all users"

    def test_get_user_none_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=True,
            display_name=DisplayNames.nobody
        )

        assert len(response) > 0, "No selectors found for no userss"

    def test_get_all_resources_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=False,
            display_name=DisplayNames.everything
        )

        assert len(response) > 0, "No selectors found for all resources"

    def test_get_none_resources_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=False,
            display_name=DisplayNames.nothing
        )
        assert len(response) > 0, "No selectors found for all resources"

    def test_negative_get_user_all_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=True,
            display_name=DisplayNames.everyone
        )

        assert response == self.permissions.get_everyone_user_selectors(
            org_id=test_org), "No selectors found for all users"

    def test_negative_get_user_none_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=True,
            display_name=DisplayNames.nobody
        )

        assert response == self.permissions.get_nobody_user_selectors(
            org_id=test_org), "No selectors found for all users"

    def test_negative_get_all_resources_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=False,
            display_name=DisplayNames.everything
        )

        assert response == self.permissions.get_everything_resource_selectors(
            org_id=test_org), "No selectors found for all users"

    def test_negative_get_none_resources_specific_connector(self):
        response = self.permissions.get_specific_selectors(
            org_id=test_org,
            user=False,
            display_name=DisplayNames.nothing
        )

        assert response == self.permissions.get_nothing_resource_selectors(
            org_id=test_org), "No selectors found for all users"

    def test_delete_rule(self):
        response = self.permissions.add_rule(
            org_id=test_org,
            domain=Domains.dataset,
            effect=Effects.allow,
            verb=Verbs.write,
            userSelector=1,
            resourceSelector=3
        )

        resp_delete = self.permissions.delete_rule(
            org_id=test_org,
            rule_id=response["data"]["permissions"]["addRule"]
        )

        assert resp_delete["data"]["permissions"]["deleteRule"], resp_delete
