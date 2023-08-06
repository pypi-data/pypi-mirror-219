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
Contains methods to interact with organization api
"""

import json
import uuid

from unify.apirequestsmng import ApiRequestManager
from unify.properties import Properties
from unify.properties import ClusterSetting
from unify.helpers.SingleOrg import single_org


class OrgAdmin(ApiRequestManager):
    """
    Class to interact with organization endpoints
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(self, cluster=None, props=Properties(ClusterSetting.KEY_RING), org_id=None):
        """
        Class constructor

        :param cluster: Cluster name to be used
        :type cluster: name
        :param props: Properties instantiated object
        :type props: class:`unify.properties.Properties`
        """

        super().__init__(cluster=cluster, props=props, org_id=org_id)

        try:

            remote = self.props.get_remote(self.cluster)

            self.orgs_api_url = remote + 'api/management/v1/orgs'
            self.org_api_url = remote + 'api/management/v1/orgs/{}'
            self.org_info_url = remote + 'api/v1/orgs/{}'
            self.who_ami_url = remote + 'api/whoami'
            self.org_sensor_analytics = remote + "api/v1/orgs/{}/sensor_diagnostics"
            self.change_group_url = remote + "api/authz/v1/groups/{}/users"
            self.all_users_url = remote + "api/v1/users"
            self.machine_user_url = remote + "api/v1/orgs/{}/machine_users"
            self.all_users_on_org = remote + "api/v1/orgs/{}/users"
            self.all_groups_url = remote + "api/authz/v1/groups"

        except Exception as error:
            raise error

    @single_org
    def get_org_info(self, org_id=None):
        """
        Retrieves the org info

        :param org_id: Org id to be queried
        :type org_id: id or str
        :return: List of information on the organization
        """

        self.verify_properties(cluster_name=self.cluster)

        headers = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        jobs = self.session.get(
            self.org_info_url.format(org_id),
            headers=headers
        )

        return json.loads(jobs.content), jobs.status_code

    @single_org
    def submit_sensor_diagnostics(self, org_id=None, *, content):
        """
        Create a request to the sensor diagnostics endpoint

        :param org_id: Organization where the sensor diagnostics will be submitted
        :param content: sensot diagnostics data
        :return: Results of the sensor diagnostics request
        """
        try:

            header = self.build_header(
                aut_token=self.props.get_auth_token(cluster=self.cluster),
                others=self.content_type_header
            )

            submit_report = self.session.put(
                self.org_sensor_analytics.format(org_id),
                headers=header,
                data=content
            )

            if submit_report.status_code == 200:
                return json.loads(submit_report.content)

            raise Exception(submit_report.content)

        except Exception as error:

            raise error

    def create_organization(self, org_name):
        """
        Creates an organization with the given name

        :param org_name: Name or organization to be created
        :type org_name: str
        :return: Server response or exception if org name already exists
        """

        try:

            if org_name is None:
                org_name = str(uuid.uuid4())

            header = self.build_header(
                aut_token=self.props.get_auth_token(cluster=self.cluster),
                others=self.content_type_header
            )

            payload = {
                "name": str(org_name),
                "piTagExportLimit": self.pi_tag_export_limit,
            }

            org_create_post = self.session.post(
                self.orgs_api_url,
                headers=header,
                data=json.dumps(payload)
            )

            if org_create_post.status_code == 200:
                return json.loads(org_create_post.content)["id"]

            raise Exception(org_create_post.content)

        except Exception as error:

            raise error

    @single_org
    def delete_organization(self, org_id=None):
        """
        Deletes the org that matched the given org id

        :param org_id: Org id to be deleted
        :type org_id: int or str
        :return: Delete successful message
        """
        try:

            delete_endpoint = self.props.get_remote(
                cluster=self.cluster
            ) + 'api/management/v1/orgs/' + str(org_id)

            header = self.build_header(
                aut_token=self.props.get_auth_token(cluster=self.cluster),
                others=self.content_type_header
            )

            delete_request = self.session.delete(
                delete_endpoint,
                headers=header
            )

            if delete_request.status_code == 200:
                return json.loads(delete_request.content)

            raise Exception(json.loads(delete_request.content))

        except Exception as error:
            raise error

    @single_org
    def invite_user(self, org_id=None, *, email, name, role):
        """
        Adds an user to the given org

        :param org_id: Org id where the user is going to be added
        :type org_id: int or str
        :param email: User's email
        :type email: str
        :param name: User's Name
        :type name: str
        :param role: User role. Accepts "Admin" or "Contributor"
        :type role: str
        :return: Invite user status message
        """
        try:

            invite_user_url = self.org_info_url.format(org_id) + '/users'

            header = self.build_header(
                org_id=org_id,
                aut_token=self.props.get_auth_token(cluster=self.cluster),
                others=self.content_type_header
            )

            payload = {"fullName": name, "email": email, "roleNames": [role]}

            invite_user_post = self.session.post(
                invite_user_url,
                headers=header,
                data=json.dumps(payload)
            )

            if invite_user_post.status_code == 201:
                return json.loads(invite_user_post.content)

            raise Exception(json.loads(invite_user_post.content))

        except Exception as error:

            raise error

    @single_org
    def invite_machine_user(self, org_id=None, *, id, password, fullname, role):
        """
        Invites a machine user

        :param org_id: Org identification where the user is going to be added
        :type org_id: int or str
        :param id: User's ID
        :type id: int or str
        :param password: User's Password
        :type password: str
        :param role: User role. Accepts "Admin" or "Contributor"
        :type role: str
        :return: Invite machine user status message
        """
        try:

            invite_machine_user_url = self.machine_user_url.format(org_id)

            header = self.build_header(
                org_id=org_id,
                aut_token=self.props.get_auth_token(cluster=self.cluster),
                others=self.content_type_header
            )

            payload = {
                "identifier": id,
                "password": password,
                "roleNames": [role],
                "fullName": fullname
            }

            invite_user_post = self.session.post(
                invite_machine_user_url,
                headers=header,
                data=json.dumps(payload)
            )

            if invite_user_post.status_code == 200:
                return json.loads(invite_user_post.content)

            raise Exception(json.loads(invite_user_post.content))

        except Exception as error:
            raise error

    def change_machine_user_password(self, org_id, id, password):
        change_password_url = self.machine_user_url.format(org_id) + "/{}".format(id)
        header = self.build_header(
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        payload = {
            "newPassword": password,
        }

        change_password_put = self.session.put(
            change_password_url,
            headers=header,
            data=json.dumps(payload)
        )

        if change_password_put.status_code == 200:
                return json.loads(change_password_put.content)
        else:
            raise Exception(json.loads(change_password_put.content))

    def get_org_list(self):
        """
        Retrieves the org list of the current cluster, only the ones whos users has logged in

        :return: List of organizations
        """
        try:

            header = self.build_header(
                aut_token=self.props.get_auth_token(cluster=self.cluster)
            )

            request = self.session.get(
                self.who_ami_url,
                headers=header
            )

            if request.status_code == 200:
                return json.loads(request.content)["organizations"]

            raise Exception(request.content)

        except Exception as error:
            raise error

    @single_org
    def update_org_metadata(self, org_id, metadata, merge=True):
        """
        Update metadata for an an existing organization.

        * Can either overwrite whole metadata object, or patch into an existing
        (or empty, it's an upsert) organization.
        * If the types mismatch, and you specify merge=True this method throw
        an error. `merge=False` will overwrite the existing contents. Type
        mismatch is either assigning a scalar to an object/list, or vice versa.
        * If the metadata field in the object is not present, it will be treated
        like an empty object.

        Examples:

        If an existing org looks something like this:
        ```
        {
            // Stuff here
            metadata: {
                "baz": {
                    "biz": "buz"
                }
            }
        }
        ```

        This `o.update_org_metadata(81, '{"baz": {"bam": "batman"}}')` will
        yield this org:
        ```
        {
            // Stuff here
            metadata: {
                "baz": {
                    "biz": "buz",
                    "bam": "batman"
                }
            }
        }
        ```

        When merge is set to false, the results are different.

        This `o.update_org_metadata(81, '{"baz": {"bam": "batman"}}', merge=False)`
        will yield this org:
        ```
        {
            // Stuff here
            metadata: {
                "baz": {
                    "bam": "batman"
                }
            }
        }
        ```

        :param org: Operates on the specified org id
        :param metadata: Contents (json string) of the metadata field on an
                         org. Does not include the key, "metadata"
        :param merge: Boolean indicating whether to merge into the existing
                      metadata object or replace the contents.
        :return:
        """

        header = self.build_header(
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        organization_url = self.org_api_url.format(org_id)

        metadata = json.loads(metadata)

        try:

            org_info, status_code = self.get_org_info(org_id)

            if status_code not in [200, 201]:
                raise Exception(org_info)

            old_metadata = org_info.get("metadata", {})

            if merge:
                def meta_merge(new_m, old_m, path_acc):
                    def cmp(comp_type):
                        return isinstance(new_m, comp_type) and isinstance(old_m, comp_type)

                    if cmp(str) or cmp(int) or cmp(float) or cmp(complex):
                        return new_m

                    if cmp(dict):
                        for k in new_m.keys():
                            old_m[k] = meta_merge(new_m[k], old_m.get(k, {}), path_acc + [k])
                        return new_m

                    raise Exception("Type mismatch, cowardly refusing to proceed. at "
                                    + '.'.join(path_acc) + " Got new type: "
                                    + str(type(new_m)) + " old type: " + str(type(old_m)))
                metadata = meta_merge(metadata, old_metadata, [])
            else:
                pass # Just use the metadata we were passed

            org_info['metadata'] = metadata
            request = self.session.put(organization_url, data=json.dumps(org_info), headers=header)

            if request.status_code in [200, 201]:
                return json.loads(request.content)

            raise Exception(request.content)

        except Exception as error:
            raise error

    @single_org
    def rename_organization(self, org_id=None, *, new_name):
        """
        Rename an existing organization

        :param org: Org id to rename
        :param new_name: New name to set to the org
        :return:
        """

        header = self.build_header(
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        organization_url = self.org_api_url.format(org_id)

        payload = {"id": org_id, "name": new_name}

        try:

            request = self.session.put(organization_url, data=json.dumps(payload), headers=header)

            if request.status_code in [200, 201]:
                return json.loads(request.content)

            raise Exception(request.content)

        except Exception as error:
            raise error

    @single_org
    def extend_expiration(self, org_id=None, *, days):
        """
        Extend organization time

        :param org_id: Org id to rename
        :param days: Days until org expires
        :return:
        """

        header = self.build_header(
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        organization_url = self.org_api_url.format(org_id)

        payload = {"id": org_id, "expiry": days}

        try:

            request = self.session.put(organization_url, data=json.dumps(payload), headers=header)

            if request.status_code in [200, 201]:
                return json.loads(request.content)

            raise Exception(request.content)

        except Exception as error:
            raise error

    def move_user_to_group(self, user_id, group_id):
        """
        Change user to a given group
        :param user_id:
        :param group_id:
        :return:
        """

        try:

            header = self.build_header(
                aut_token=self.props.get_auth_token(cluster=self.cluster),
                others=self.different_content_type
            )

            invite_user_post = self.session.post(
                self.change_group_url.format(group_id),
                headers=header,
                data=str(user_id)
            )

            if invite_user_post.status_code in range(200, 201):
                return json.loads(invite_user_post.content)

            raise Exception(json.loads(invite_user_post.content))

        except Exception as error:

            raise error

    def retrieve_all_users(self):
        """
        Retrieves all users who the loged in user can retrieve
        :return:
        """
        try:
            all_users_list = self.simple_get(final_url=self.all_users_url)

            if all_users_list.status_code in range(200, 201):
                return json.loads(all_users_list.content)

            raise Exception(json.loads(all_users_list.content))

        except Exception as error:

            raise error

    def retrieve_all_users_form_org(self, org_id):
        """
        Retrieves all users who the loged in user can retrieve
        :return:
        """
        try:
            all_users_list = self.simple_get(final_url=self.all_users_on_org.format(org_id))

            if all_users_list.status_code in range(200, 201):
                return json.loads(all_users_list.content)

            raise Exception(json.loads(all_users_list.content))

        except Exception as error:

            raise error

    def get_all_groups(self):
        """

        :return:
        """
        try:
            all_users_list = self.simple_get(final_url=self.all_groups_url)

            if all_users_list.status_code in range(200, 201):
                return json.loads(all_users_list.content)

            raise Exception(json.loads(all_users_list.content))

        except Exception as error:

            raise error
