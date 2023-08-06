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


class Users(ApiRequestManager):
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

        self.session.headers.update(
            {
                self.x_auth_token_header: self.props.get_auth_token(cluster=self.cluster)
            }
        )

        remote = self.props.get_remote(self.cluster)

        self.home_url = remote + 'api/v1/users'

        self.users_url = self.home_url + '/{}'

        self.password_url = self.users_url + '/password'

    @single_org
    def change_user_password(self, org_id=None, *, user_id, old_password, new_password):
        body = {"newPassword": new_password, "oldPassword": old_password}

        if org_id is not None:
            headers = self.build_header(
                org_id=org_id,
                others=self.content_type_header
            )
        else:
            headers = self.build_header(
                others=self.content_type_header
            )

        request = self.session.put(
            self.password_url.format(user_id),
            headers=headers,
            json=body
        )

        if request.status_code in self.OK:
            return json.loads(request.content)

        raise Exception(request.content.decode())

    @single_org
    def get_users_list(self, org_id=None, *, user_ids: list):

        data = tuple(["userId", user_id] for user_id in user_ids)

        if org_id is not None:
            headers = self.build_header(
                org_id=org_id,
                others=self.content_type_header
            )
        else:
            headers = self.build_header(
                others=self.content_type_header
            )

        request = self.session.get(
            self.home_url,
            headers=headers,
            params=data
        )

        if request.status_code in self.OK:
            return json.loads(request.content)

        raise Exception(request.content.decode())

    @single_org
    def delete_user(self, org_id=None, *, user_id):

        if org_id is not None:
            headers = self.build_header(
                org_id=org_id,
                others=self.content_type_header
            )
        else:
            headers = self.build_header(
                others=self.content_type_header
            )

        request = self.session.delete(
            self.users_url.format(user_id),
            headers=headers,
        )

        if request.status_code in self.OK:
            return json.loads(request.content)

        raise Exception(request.content.decode())
