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
Contains methods to interact with Unify datasets api
"""
import json
import time
import uuid
import os
from tempfile import mkstemp

from unify.properties import Properties, ClusterSetting
from .apirequestsmng import ApiRequestManager
from .generalutils import csv_to_json
from .generalutils import json_to_csv
from .generalutils import create_schema_dataset
from .generalutils import stream_iterable
from .WaitingLibrary import Wait
from unify.helpers.SingleOrg import single_org
from unify.helpers.graph_ql.dataset_gql import DatasetGrapql


class Sources(ApiRequestManager):
    """
    Class to interact with dataset endpoints
    """

    def __init__(self, cluster=None, props=Properties(ClusterSetting.KEY_RING), org_id=None, session=None):
        """
        Class constructor

        :param cluster: Hostname
        :type cluster: str
        :param props: Instantiated Properties class
        :type props: class:`unify.properties.Properties`
        """

        super().__init__(cluster=cluster, props=props, org_id=org_id, session=session)

        try:

            self.epoch_time = int(time.time())
            self.sources_url = self.props.get_remote(self.cluster) + "io/v1/org/{}/sources"

            self.agents_url = self.props.get_remote(self.cluster) + "agents/v2/"

            self.piwebapi_test_url = self.agents_url + "piwebapi/org/{}/test"

            self.piwebapi_create_url = self.agents_url + \
                                       "piwebapi/org/{}/create?modeldata_only=true"

            self.piconfig_upload_url = self.agents_url + "piconfig/org/{}/model/?name=&serverName="

            self.piconfig_upload_url_no_params = self.agents_url + "piconfig/org/{}/model/"

            self.staticfile_upload_url = self.agents_url + "staticfile/org/{}/model"

            self.delete_source_url = self.agents_url + "piwebapi/org/{}/source/{}"

            self.stage_file_url = self.props.get_remote(self.cluster) + "datasets/v1/stage/file"

            self.post_data_set_schema_url = self.props.get_remote(
                self.cluster) + "datasets/v1/dataset"

            self.commit_data_set_url = self.props.get_remote(
                self.cluster) + "datasets/v1/dataset/{}/commit"

            self.labeling_sources = self.props.get_remote(
                self.cluster) + "datasets/v1/labeling"

            self.labeling_sources_2 = self.props.get_remote(
                self.cluster) + "datasets/v1/labeling/query"

            self.labeling_sources_facets_url = self.props.get_remote(
                self.cluster) + "datasets/v1/labeling/facets"

            self.append_url = self.props.get_remote(
                self.cluster) + "agents/v2/staticfile/org/{}/model/{}/append"

            self.download_dataset_url = self.props.get_remote(
                self.cluster) + "tags/org/{}/datasets/{}/download"

            self.get_commit = self.commit_data_set_url + "/{}"

            self.preview_source_url = self.props.get_remote(
                self.cluster) + "tags/org/{}/datasets/{}/preview"

            self.dataset_info_url = self.props.get_remote(
                self.cluster) + "datasets/v1/dataset/{}/info"

            self.gql_builder = DatasetGrapql()

            # Datastreams
            self.datastream_events_info_url = self.props.get_remote(
                self.cluster) + "datasets/v1/dataset/{}/events"

            self.datastream_download_events = self.props.get_remote(
                self.cluster) + "datasets/v1/dataset/{}/events/download"

        except Exception as error:
            raise error

    def get_status(self, org_id, dataset_id, commit_id):
        """
        Retrieves the status of the given commit id

        :param org_id: Org where the commit has occurred
        :type org_id: int or str
        :param dataset_id: Datasets id of whom the commit belongs to
        :type dataset_id: str
        :param commit_id: Commit id to be retrieved
        :type commit_id: str
        :return:
        """
        return self.get_commit_status(org_id=org_id, data_set_id=dataset_id, commit_id=commit_id)[0]

    def accert_status(self, org_id, dataset_id, commit_id, expected):
        """
        Accerts that the status of a given commit is what is expected

        :param org_id: Org where the commit has occurred
        :type org_id: int or str
        :param dataset_id: Dataset id of whom the commit belongs to
        :type dataset_id: str
        :param commit_id: Commit id to be retrieved
        :type commit_id: str
        :param expected: Expected status
        :type expected: str
        :return:
        """
        status = self.get_status(org_id=org_id, dataset_id=dataset_id, commit_id=commit_id)

        if "status" in status:

            tipe = status["status"]

            if "$type" in tipe:
                return expected in tipe["$type"]

        return False

    def is_commit_completed(self, org_id, dataset_id, commit_id):
        """
        Verifies that the status of the commit is completed

        :param org_id: Org where the commit has occurred
        :type org_id: int or str
        :param dataset_id: Dataset id of whom the commit belongs to
        :type dataset_id: str
        :param commit_id: Commit id to be asserted
        :type commit_id: str
        :return:
        """
        return self.accert_status(
            org_id=org_id,
            dataset_id=dataset_id,
            commit_id=commit_id,
            expected="Completed"
        )

    def divide_dataset_in(
            self, name, org_id, content, format="csv",
            convert_to_parquet="false", encoding='UTF-8', chunks=10000):
        """
        Upload a dataset through the static route. This method should be used when
        uploading a big file. It will split the file into
        smaller chunks and upload them sequentially.

        :param name: Dataset name to be cerated
        :type name: str
        :param org_id: Org where the dataset will be created
        :type org_id: int or str
        :param content: Dataset content
        :type content: str
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert file to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: File encoding
        :type encoding: str, optional
        :param chunks: Number of chunks to split the file
        :type chunks: int
        :return:
        """

        data = content.encode(encoding)

        jdata = csv_to_json(data)

        dataset_data = {}
        index = 0
        for aux_file in stream_iterable(container=jdata, chunk=chunks):
            aux_name = "{}_{}".format(name, index)

            file_dir, path = mkstemp(suffix=".csv")

            open(path, "w+").write(json_to_csv(aux_file))

            dataset_data[aux_name] = self.create_api_data_set(
                name=aux_name,
                org_id=org_id,
                file_path=path,
                format=format,
                convert_to_parquet=convert_to_parquet,
                encoding=encoding
            )

            Wait().until(
                self.is_commit_completed,
                "commit {} never completed".format(dataset_data[aux_name]["data_set_id"]),
                org_id,
                dataset_data[aux_name]["data_set_id"],
                dataset_data[aux_name]["commit_id"]
            )

            os.close(file_dir)
            index += 1

        return dataset_data

    @single_org
    def upload_big_dataset(
            self, name, org_id=None, *, content, format="csv",
            convert_to_parquet="false", encoding='UTF-8', chunks=10000):
        """
        Upload a dataset through the static route. This method should be used when
        uploading a big file. It will split the file into
        smaller chunks and upload them sequentially.

        :param name: Dataset name to be cerated
        :type name: str
        :param org_id: Org where the dataset will be created
        :type org_id: int or str
        :param content: Dataset content
        :type content: str
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert file to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: File encoding
        :type encoding: str, optional
        :param chunks: Number of chunks to split the file
        :type chunks: int
        :return:
        """

        data = content.encode(encoding)

        jdata = csv_to_json(data, encoding=encoding)

        first = True

        dataset_data = {
            "create": {},
            "append": []
        }
        for aux_file in stream_iterable(container=jdata, chunk=chunks):

            if first:

                first = False

                file_dir, path = mkstemp(suffix=".csv")

                open(path, "w", encoding=encoding).write(json_to_csv(aux_file))

                dataset_data["create"] = self.create_api_data_set(
                    name=name,
                    org_id=org_id,
                    file_path=path,
                    format=format,
                    convert_to_parquet=convert_to_parquet,
                    encoding=encoding
                )

                Wait().until(
                    self.is_commit_completed,
                    "commit {} never completed".format(dataset_data["create"]["data_set_id"]),
                    org_id,
                    dataset_data["create"]["data_set_id"],
                    dataset_data["create"]["commit_id"]
                )

                os.close(file_dir)

            else:

                file_dir, path2 = mkstemp(suffix=".csv")

                open(path2, "w", encoding=encoding).write(json_to_csv(aux_file))

                try:
                    added_data = self.add_data_to_existing_source(
                        name="{} {}".format(name, str(uuid.uuid4())[:4]),
                        org_id=org_id,
                        data_set_id=dataset_data["create"]["data_set_id"],
                        file_path=path2,
                        group_id=dataset_data["create"]["group_id"]
                    )

                    Wait().until(
                        self.is_commit_completed,
                        "commit {} never completed".format(dataset_data["create"]["data_set_id"]),
                        org_id,
                        dataset_data["create"]["data_set_id"],
                        added_data["commit_id"]
                    )

                    dataset_data["append"].append(added_data)

                    os.close(file_dir)

                except Exception as err:
                    print("skipping {}".format(repr(err)))

        return dataset_data

    @single_org
    def create_api_data_set(
            self,
            name,
            org_id=None,
            *,
            file_path,
            format="csv",
            convert_to_parquet="false",
            encoding="UTF-8"
    ):

        """
        Creates a dataset through the static file route.

        :param name: Name to of the new dataset
        :type name: str
        :param org_id: Org id where the dataset will be stored
        :type org_id: int or str
        :param file_path: Directory file path where the dataset contents are
        :type file_path: str
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: Source file encoding
        :type encoding: str, optional
        :return:
        """

        if file_path is None:
            raise Exception("File Path must not be None")

        content = open(file_path, "rb").read().decode(encoding)

        return self.create_api_data_set_with_content(
            name=name,
            org_id=org_id,
            content=content,
            format=format,
            convert_to_parquet=convert_to_parquet,
            encoding=encoding
        )

    @single_org
    def create_api_data_set_with_content(
            self,
            name,
            org_id=None,
            *,
            content,
            format="csv",
            convert_to_parquet="false",
            encoding="UTF-8"):
        """
        Creates a dataset through the static file route.

        :param name: Name of the new dataset
        :type name: str
        :param org_id: Org id where the dataset will be stored
        :type org_id: int or str
        :param content: dataset content in csv or tsv format
        :type content: str
        :param format: Content format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: Content encoding
        :type encoding: str, optional
        :return:
        """
        results = {}

        stage_result = self.stage_file_with_content(
            name=name,
            org_id=org_id,
            file_data=content,
            format=format,
            convert_to_parquet=convert_to_parquet,
            encoding=encoding
        )

        results["group_id"] = stage_result

        schema = create_schema_dataset(
            csv_data=content,
            name=name
        )
        initial_commit = self.post_file_schema(
            org_id=org_id,
            schema_data=json.dumps(schema),
        )

        results["data_set_id"] = initial_commit["id"]
        results["commit_id"] = initial_commit["commitId"]

        second_commit = self.append_command(
            org_id=org_id,
            data_set_id=results["data_set_id"],
            name=name,
            group_id=results["group_id"]
        )

        results.update(second_commit)

        return results

    @single_org
    def append_all(self, name, org_id=None, *, file_path, format="csv",
                   convert_to_parquet="false", encoding='UTF-8', chunks=10000, existing_dataset_id=None):
        """

        This method will split a data-set into chunks, and uplaod chunk by chunk. This is usefull for
        limiting and not overwelm the unify cluster. Use this method when trying to upload big datasets.

        :param name: Dataset name to be cerated
        :type name: str
        :param org_id: Org where the dataset will be created
        :type org_id: int or str
        :param file_path: Dataset file directory route
        :type file_path: str
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert file to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: File encoding
        :type encoding: str, optional
        :param chunks: Number of chunks to split the file
        :type chunks: int
        :return:
        """

        content = open(file_path, "rb").read().decode(encoding)

        data = content.encode(encoding)

        jdata = csv_to_json(data, encoding=encoding)

        first = True if existing_dataset_id is None else False

        dataset_data = {
            "create": {},
            "append": []
        }

        all_groups = []

        any_stage = False

        dataset_id = None if existing_dataset_id is None else existing_dataset_id

        for aux_file in stream_iterable(container=jdata, chunk=chunks):

            if first:

                first = False

                file_dir, path = mkstemp(suffix=".csv")

                open(path, "w", encoding=encoding).write(json_to_csv(aux_file))

                dataset_data["create"] = self.create_api_data_set(
                    name=name,
                    org_id=org_id,
                    file_path=path,
                    format=format,
                    convert_to_parquet=convert_to_parquet,
                    encoding=encoding
                )

                dataset_id = dataset_data["create"]["data_set_id"]

                Wait().until(
                    self.is_commit_completed,
                    "commit {} never completed".format(dataset_data["create"]["data_set_id"]),
                    org_id,
                    dataset_data["create"]["data_set_id"],
                    dataset_data["create"]["commit_id"]
                )

                os.close(file_dir)

            else:

                try:
                    stage_name = "file_{}".format(str(uuid.uuid4())[:5])

                    if len(json_to_csv(aux_file)):
                        stage_result = self.stage_file_with_content(
                            name=stage_name,
                            org_id=org_id,
                            file_data=json_to_csv(aux_file),
                            format=format,
                            convert_to_parquet=convert_to_parquet,
                            encoding=encoding
                        )

                        print(stage_result.decode())

                        all_groups.append(
                            {
                                "groupId": stage_result.decode(),
                                "name": stage_name
                            }
                        )

                        any_stage = True

                except Exception as err:
                    print("skipping {}".format(repr(err)))

        if any_stage:
            dataset_data["append"] = self.append_all_command(
                org_id=org_id,
                files=all_groups,
                data_set_id=dataset_id
            )

        return dataset_data

    @single_org
    def get_commit_status(self, org_id=None, *, data_set_id, commit_id):
        """
        Retrieves the status of the given commit id.

        :param org_id: Org id where the commit has occurred
        :type org_id: int or str
        :param dataset_id: Datasets id of whom the commit belongs to
        :type dataset_id: str
        :param commit_id: Commit id to be retrieved
        :type commit_id: str
        :return:
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others={"'Content-Type'": "application/data"}
        )

        url = self.get_commit.format(data_set_id, commit_id)

        test_request = self.session.get(url, headers=header)

        return json.loads(test_request.content.decode('utf8')), test_request.status_code

    @single_org
    def download_dataset_content(self, org_id=None, *, dataset_id):
        """
        Downloads the content of a given dataset.

        :param org_id: Org id where the dataset exists
        :type org_id: int or str
        :param dataset_id: Dataset id to be retrieved
        :type dataset_id: str
        :return:
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )

        get_source_request = self.session.get(
            self.download_dataset_url.format(org_id, dataset_id),
            headers=header
        )

        if get_source_request.status_code == 200:
            return get_source_request.content

        raise Exception(repr(get_source_request.content))

    @single_org
    def create_export_dataset(self, org_id=None, *, dataset_ids):
        """
        Create the content needed to export a dataset.
        This is usually used when using the import dataset.

        :param org_id: Org id where the dataset exists
        :type org_id: int or str
        :param dataset_ids: List containing the dataset ids
        :type dataset_ids: list of str
        :return:
        """
        datasets = self.get_sources(org_id=org_id)

        id_to_type = {}

        for dataset in datasets:
            id_to_type[dataset["id"]["id"]] = dataset

        all_datasets = []
        for dataset_id in dataset_ids:

            if dataset_id not in id_to_type:
                continue

            info = id_to_type[dataset_id]

            source_type = "Upload"

            if "labels" in info:
                if "raw" in info["labels"]:
                    if "ean_source_type" in info["labels"]["raw"]:
                        source_type = info["labels"]["raw"]["ean_source_type"]

            get_source_request = self.download_dataset_content(org_id=org_id, dataset_id=dataset_id)

            result = {
                "component": None,
                "id": dataset_id,
                "schema": info["schema"],
                "name": id_to_type[dataset_id]["name"],
                "type": source_type,
                "file_content": csv_to_json(csv_data=get_source_request)
            }

            all_datasets.append(result)

        return json.dumps(all_datasets)

    @single_org
    def add_data_content_to_existing_source(
            self, name, org_id=None, *, content,
            data_set_id, group_id=None, format="csv"):
        """
        Helper function to append data to existing dataset

        :param name: Name of the current file, used for staging the file
        :type name: str
        :param org_id: Org id where the target dataset exists
        :type org_id: int or str
        :param content: content of append data
        :param data_set_id: Dataset id where the content will be appended
        :type data_set_id: int or str
        :param group_id: Group identification that the dataset belongs
        :type group_id: str
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :return:
        """
        results = {}

        stage = self.stage_file_with_content(
            name=name,
            org_id=org_id,
            file_data=content,
            group_id=group_id,
            format=format,
        )

        results["group_id"] = stage

        final_commit = self.append_command(
            org_id=org_id,
            data_set_id=data_set_id,
            name=name,
            group_id=results["group_id"]
        )

        results.update(final_commit)

        return results

    @single_org
    def add_data_to_existing_source(
            self, name, org_id=None, *, file_path,
            data_set_id, group_id=None, format="csv"):
        """
        Helper function to append data to existing dataset

        :param name: Name of the current file, used for staging the file
        :type name: str
        :param org_id: Org id where the target dataset exists
        :type org_id: int or str
        :param file_path: Directory file path that contains the data to be appended
        :type file_path: str
        :param data_set_id: Dataset id where the content will be appended
        :type data_set_id: int or str
        :param group_id: Group identification that the dataset belongs
        :type group_id: str
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :return:
        """
        results = {}

        second_stage = self.stage_data(
            name=name,
            org_id=org_id,
            file_path=file_path,
            group_id=group_id,
            format=format
        )

        results["group_id"] = second_stage

        final_commit = self.append_command(
            org_id=org_id,
            data_set_id=data_set_id,
            name=name,
            group_id=results["group_id"]
        )

        results.update(final_commit)

        return results

    @single_org
    def overwrite_dataset(
            self, org_id=None, *, data_set_id, file_path, group_id=None,
            format="csv", convert_to_parquet="false", encoding="utf-8", encode=True):

        """
        Overwrites the contents of the given dataset with new content.

        :param org_id: Org id where the target dataset exists
        :type org_id: int or str
        :param data_set_id: Dataset id that its content will be overwritten
        :type data_set_id: str
        :param file_path: Directory file path that contains the data to be appended
        :type file_path: str
        :param group_id: Group identification that the dataset belongs
        :type group_id: str, optional
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert file to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: Encoding of the file
        :type encoding: int or str
        :return:
        """
        response = {}

        name = "overwirte{}".format(int(time.time()))

        response["stage"] = self.stage_data(
            name=name,
            org_id=org_id,
            file_path=file_path,
            group_id=group_id,
            format=format,
            convert_to_parquet=convert_to_parquet,
            encoding=encoding,
            encode=encode
        )
        command = {
            "commands":
                [
                    self.single_overwrite_command(group_id=response["stage"], name=name)
                ]
        }
        response["overwrite"] = self._commit_dataset_command(org_id, data_set_id, command)

        return response

    def _commit_dataset_command(self, org_id, data_set_id, command):
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others={"'Content-Type'": "application/data"}
        )

        headers = dict(header.items())
        request = self.session.post(
            url=self.commit_data_set_url.format(data_set_id),
            headers=headers,
            json=command
        )

        if request.status_code in [200, 202]:
            append = json.loads(request.content)

            Wait(200).until(
                self.is_commit_completed,
                "commit {} never completed".format(data_set_id),
                org_id,
                data_set_id,
                append["commit_id"]
            )

            return append
        else:
            raise Exception("commit to {} fails".format(data_set_id) + repr(request.content))

    @single_org
    def truncate_data_set(self, org_id=None, *, data_set_id):
        """
        Truncates the dataset content.

        :param org_id: Org where the target dataset exists
        :type org_id: int or str
        :param data_set_id: Dataset id where which contents will be truncated
        :type data_set_id: str
        :return:
        """
        command = {"commands": [{"$type": "truncate", "cause": []}]}
        return self._commit_dataset_command(org_id, data_set_id, command)

    @single_org
    def append_dataset(self, org_id=None, *, data_set_id, content):
        """
        Appends data to existing dataset.

        :param org_id: Org where the target dataset exists
        :type org_id: int or str
        :param data_set_id: Dataset id where the content will be appended
        :type data_set_id: str
        :param content: Data content that will be added to the dataset
        :type content: str
        :return:
        """
        file_dir, path = mkstemp(suffix=".csv")

        open(path, "wb").write(content.encode())

        os.close(file_dir)

        headers = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )

        files = {'file': open(path, "rb")}

        post_upload_file = self.session.post(
            self.append_url.format(org_id, data_set_id),
            headers=headers,
            files=files
        )

        if post_upload_file.status_code in [200, 201, 202]:
            response = json.loads(post_upload_file.content)

            return response

        raise Exception(repr(post_upload_file.content))

    def label(self, org_id, data_set_id, labels):
        """
        Method to create dataset event object
        :param org_id: Org where the event will be applied
        :param data_set_id: dataset identification where the event would be applied
        :param labels: labels that will be added to this event
        :return:
        """
        command = {
            "commands":
                [
                    {
                        "$type": "text-label-group",
                        "key": "ean.facets",
                        "values": labels,
                        "cause": [],
                    }
                ]
        }
        return self._commit_dataset_command(org_id, data_set_id, command)

    def append_command(self, org_id, data_set_id, group_id, name):
        """
        Executes append command to a staged file on a group id.

        :param org_id: Org where the target dataset exists
        :type org_id: int or str
        :param data_set_id: Dataset id to be appended
        :type data_set_id: str
        :param group_id: Group identification that the dataset belongs
        :param name: Name of the staged file
        :type name: str
        :return:
        """
        command = {
            "commands":
                [
                    self.single_append_command(group_id=group_id, name=name)
                ]
        }
        return self._commit_dataset_command(org_id, data_set_id, command)

    def append_all_command(self, org_id, data_set_id, files: list):

        command = {
            "commands":
                [
                    {
                        "$type": "append-all",
                        "files": files,
                        "overwrite": False,
                        "cause": []
                    }
                ]
        }

        open("append_all.json", "w+").write(json.dumps(command))
        return self._commit_dataset_command(org_id, data_set_id, command)

    def stage_data(
            self, name, org_id, file_path, group_id=None, format="csv",
            convert_to_parquet="false", encoding='UTF-8', encode=True):
        """
        Stages data to a given org and group id.

        :param name: Name of the staged file
        :type name: str
        :param org_id: Org where the target dataset exists
        :type org_id: int or str
        :param file_path: Directory file path with files to be staged
        :type file_path: str
        :param group_id: Group identification that the dataset belongs
        :type group_id: str, optional
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: Dataset file encoding
        :type encoding: str, optional
        :param encode: Encode the dataset with given encoding
        :type encode: bool, optional
        :return:
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others={"'Content-Type'": "application/octet-stream"}
        )

        if group_id is None:
            payload_data = {
                "name": name,
                "convertToParquet": convert_to_parquet,
                "format": format,
                "charset": encoding
            }
        else:
            payload_data = {
                "name": name,
                "convertToParquet": convert_to_parquet,
                "format": format,
                "groupId": group_id,
                "charset": encoding
            }

        if encode:
            file_data = open(file_path, "r").read().encode(encoding)
        else:
            file_data = file_path.encode(encoding)

        test_request = self.session.post(
            self.stage_file_url,
            headers=header,
            data=file_data,
            params=payload_data
        )

        return test_request.content.decode()

    def stage_file(self, name, org_id, file_path, group_id=None, format="csv",
                   convert_to_parquet="false", encoding='UTF-8', encode=False):
        """
        Stage data from file to a given org and group id.

        :param name: Name of the staged file
        :type name: str
        :param org_id: Org where the target dataset exists
        :type org_id: int or str
        :param file_path: Directory file path with files to be staged
        :type file_path: str
        :param group_id: Group identification that the dataset belongs
        :type group_id: str, optional
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert to parquet
        :type convert_to_parquet: bool, optional
        :param encoding: Dataset file encoding
        :type encoding: str, optional
        :param encode: Encode the dataset with given encoding
        :type encode: bool, optional
        :return:
        """

        file_data = open(file_path, "r").read()

        return self.stage_file_with_content(
            name=name,
            org_id=org_id,
            file_data=file_data,
            group_id=group_id,
            format=format,
            convert_to_parquet=convert_to_parquet,
            encoding=encoding,
            encode=encode
        )

    def stage_file_with_content(
            self, name, org_id, file_data, group_id=None,
            format="csv", convert_to_parquet="false", encoding='UTF-8', encode=False
    ):
        """
        Stage data from content to a given org and group id.

        :param name: Name of the staged file
        :type name: str
        :param org_id: Org where the target dataset exists
        :type org_id: int or str
        :param file_data: Content with data to be staged
        :type file_data: str
        :param group_id: Group identification that the dataset belongs
        :type group_id: str, optional
        :param format: File format. Accepts "CSV" or "TSV"
        :type format: str, optional
        :param convert_to_parquet: Flag to convert to parquet.
        :type convert_to_parquet: bool, optional
        :param encoding: File encoding
        :type encoding: str, optional
        :param encode: Encode the dataset with given encoding
        :type encode: bool, optional
        :return:
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others={"'Content-Type'": "application/octet-stream"}
        )

        if group_id is None:

            payload_data = {
                "name": name,
                "convertToParquet": convert_to_parquet,
                "format": format,
                "charset": encoding
            }
        else:
            payload_data = {
                "name": name,
                "convertToParquet": convert_to_parquet,
                "format": format,
                "groupId": group_id,
                "charset": encoding
            }

        test_request = self.session.post(
            self.stage_file_url,
            headers=header,
            data=file_data.encode(encoding),
            params=payload_data
        )

        if test_request.status_code in [200, 202]:
            return test_request.content.decode()
        else:
            raise Exception("Failed to stage file, org {}, status code: {}, error: {}".format(org_id, test_request.status_code, test_request.content))

    def post_file_schema(self, org_id, schema_data, encoding='UTF-8'):
        """
        Posts the schema of a file to be staged.

        :param org_id: Org where the file is going to be staged
        :type org_id: int or str
        :param schema_data: File schema
        :type schema_data: dict
        :param encoding: File encoding
        :type encoding: str, optional
        :return:
        """

        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others={"'Content-Type'": "application/data"}
        )

        schema_request = self.session.post(
            self.post_data_set_schema_url,
            headers=header,
            data=schema_data.encode(encoding)
        )

        if schema_request.status_code == 200:
            results = json.loads(schema_request.content)

            Wait(200).until(
                self.is_commit_completed,
                "commit {} never completed".format(results["id"]),
                org_id,
                results["id"],
                results["commitId"]
            )
            return results

        raise Exception(repr(schema_request.content))

    def pi_config_upload(self, name, server_name, file_path, org_id):
        """
        DEPRECATED - Use static_file_upload instead! This method may be removed
        in the future on a major version bump.

        Uploads PI-CONFIG dataset.

        :param name: Dataset name
        :type name: str
        :param server_name: PI-Config data archive server name
        :type server_name: str
        :param file_path: Directory file path with files to be uploaded
        :type file_path: str
        :param org_id: Org where the dataset will be created
        :type org_id: int or str
        :return:
        """

        headers = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )

        upload_file = {'file': open(file_path, "rb")}

        query_strings = {"name": str(name), "serverName": str(server_name)}

        post_upload_pitag = self.session.post(
            self.piconfig_upload_url_no_params.format(org_id),
            params=query_strings,
            headers=headers,
            files=upload_file
        )

        if post_upload_pitag.status_code == 200:
            return json.loads(post_upload_pitag.content)

        raise Exception(repr(post_upload_pitag.content))

    @single_org
    def static_file_upload(self, name, content, org_id=None, params=None, encoding=None):
        """
        :param name: Dataset name to be created
        :type name: str
        :param content: Dataset content stored in a variable
        :type content: str
        :param org_id: Org where the dataset will be created
        :type org_id: str
        :param params: Additional http parameters
        :return:
        """

        static_file_upload_url = self.staticfile_upload_url

        query_strings = {
            "name": str(name)
        }
        if encoding:
            query_strings["charset"] = encoding

        headers = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )

        files = {'file': open(content, "rb")}

        if params is not None:
            for tup in params:
                if len(tup) == 2:
                    query_strings[tup[0]] = tup[1]

        post_upload_file = self.session.post(
            static_file_upload_url.format(org_id),
            headers=headers,
            files=files,
            params=query_strings
        )

        if post_upload_file.status_code == 200:
            return json.loads(post_upload_file.content)

        raise Exception(repr(post_upload_file.content))

    @single_org
    def get_sources(self, org_id=None, page_num=1, page_size=1000):

        """
        Retrieves all the metadata of datasets on an org.

        :param org_id: Org to be queried
        :type org_id: int or str
        :param page_num: pagination page number
        :param page_size: pagination page size
        :return:
        """

        query = self.gql_builder.build_dataset_query(
            page_num=page_num,
            page_size=page_size
        )

        get_sources_request = self.graph_ql_query(org_id=org_id, query=query)

        if get_sources_request.status_code in range(200, 203):
            data = json.loads(get_sources_request.content)

            if "data" in data:
                if "artifacts" in data["data"]:
                    return data["data"]["artifacts"]

            return []
        error_message = {
            "message": repr(get_sources_request.content),
            "code": get_sources_request.status_code
        }

        raise Exception(json.dumps(error_message))

    def get_sources_by_labels(self, org_id, facets):
        """
        Retieves all datasets that matches given labels.

        :param org_id: Org id
        :type org_id: int or str
        :param facets: List of dataset labels. Example: ["label1", "label2"]
        :type facets: list of str
        :return:
        """

        query = self.gql_builder.build_dataset_query(
            facets=facets
        )

        get_sources_request = self.graph_ql_query(org_id=org_id, query=query)

        if get_sources_request.status_code in range(200, 203):
            data = json.loads(get_sources_request.content)

            if "data" in data:
                if "artifacts" in data["data"]:
                    return data["data"]["artifacts"]

            return []

        raise Exception(repr(get_sources_request.content))

    def get_sources_by_filters(self, org_id, filters):
        """
        Retieves all datasets that matches given filters.

        :param org_id: Org id
        :type org_id: int or str
        :param filters: Dictonary with filter by name and value. Example: {'name':dataset_name}
        :type filters: dict of key value pair
        :return:
        """

        query = self.gql_builder.build_dataset_query(
            other_filters=filters
        )
        get_sources_request = self.graph_ql_query(org_id=org_id, query=query)

        if get_sources_request.status_code in range(200, 203):
            data = json.loads(get_sources_request.content)
            if "data" in data:
                if "artifacts" in data["data"]:
                    return data["data"]["artifacts"]

            return []

        raise Exception(repr(get_sources_request.content))

    @single_org
    def delete_source(self, org_id=None, *, source_id):
        """
        This method deletes a dataset that is stored on the org_id with the given source_id

        :param org_id: Organization ID where the datasets is stored
        :type org_id: int or str
        :param source_id: Data set id to be deleted
        :type source_id: str
        :return: Result of the delete operation {"message":"Success","metadata":{}}
        :raise: Exception when response code is not 200 or 201
        """

        headers = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        delete_request = self.session.delete(
            self.delete_source_url.format(
                str(org_id),
                source_id
            ),
            headers=headers
        )

        if delete_request.status_code in range(200, 203):
            return json.loads(delete_request.content)
        try:
            msg = json.loads(delete_request.content)
            raise Exception(msg)
        except json.JSONDecodeError as e:
            raise Exception(str(delete_request.content))

    @single_org
    def preview_dataset(self, org_id=None, *, dataset_id, page_num=1):

        """
        Preview the content of the dataset id give, page_num is the pagination of the given dataset
        :param org_id:
        :param dataset_id:
        :param page_num:
        :return:
        """

        headers = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        data = [("pageNum", page_num)]

        get_response = self.session.get(
            self.preview_source_url.format(org_id, dataset_id),
            headers=headers,
            params=data
        )

        if get_response.status_code in [200, 201]:
            return json.loads(get_response.content)

        try:
            msg = json.loads(get_response.content)
            raise Exception(msg)
        except json.JSONDecodeError:
            raise Exception(str(get_response.content))

    @single_org
    def get_dataset_info(self, org_id=None, *, dataset_id):

        """
        return metdadata of the desired dataset
        :param org_id:
        :param dataset_id:
        :return:
        """

        headers = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster),
            others=self.content_type_header
        )

        data = [("dataset_id", dataset_id)]

        get_response = self.session.get(
            self.dataset_info_url.format(dataset_id),
            headers=headers,
            params=data
        )

        if get_response.status_code in [200, 201]:
            return json.loads(get_response.content)

        try:
            msg = json.loads(get_response.content)
            raise Exception(msg)
        except json.JSONDecodeError:
            raise Exception(str(get_response.content))

    @single_org
    def upload_spreadsheet(self, name=None, file_path=None, org_id=None, sheet_name=None):

        """
        :param name:
        :param file_path:
        :param org_id:
        :param sheet_name: Specify the spreadsheet name where the data is located
        :return:
        """
        if sheet_name is None:
            return self.static_file_upload(
                name=name,
                content=file_path,
                org_id=org_id
            )
        else:
            return self.static_file_upload(
                name=name,
                content=file_path,
                org_id=org_id,
                params=[('sheetName', sheet_name)]
            )

    @single_org
    def update_dataset_metadata(self, org_id=None, *, dataset_id=None, name=None, description=None, facets=None):
        """
        Method to update a dataset's metadata

        :param org_id: org id where the pipeline is stored
        :param dataset_id: id of the pipeline to be edited
        :param name: new pipeline name
        :param description: description to be added
        :param facets:
        :return:
        """

        return self.update_artifact_metadata(
            org_id=org_id,
            artifact_id=dataset_id,
            artifact_type="dataset",
            name=name,
            description=description,
            facets=facets
        )

    @single_org
    def wait_for_dataset(self, org_id=None, *, dataset_id):
        """
        Wait for a dataset to be ready to be used

        :param org_id: Organization id where the dataset was created
        :param dataset_id: dataset id number
        :return:
        """
        return self.wait_for_artifact(
            org_id=org_id,
            artifact_id=dataset_id,
            artifact_type="dataset"
        )

    @single_org
    def get_datastream_events_info(self, org_id=None, *, dataset_id, sequenceNr=0):
        """
        Returns a list with all events occurred in a datastream

        :param org_id: Optional, Organization id where the dataset was created
        :param dataset_id: dataset id number
        :param sequenceNr: Optional, the number of the first event to be returned
        :return: A list with the events
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )
        params = {'fromSequenceNr': sequenceNr}
        response = self.session.get(
            self.datastream_events_info_url.format(dataset_id),
            params=params,
            headers=header
        )

        if response.status_code in self.OK:
            result = response.json()
            return result['events']

        try:
            msg = json.loads(response.content)
            raise Exception(msg)
        except json.JSONDecodeError:
            raise Exception(str(response.content))

    @single_org
    def get_datastream_event_data(self, org_id=None, *, dataset_id, sequenceNr):
        """
        Returns the data of the datastream event specified in the 'sequenceNr' param

        :param org_id: Optional, Organization id where the dataset was created
        :param dataset_id: dataset id number
        :param sequenceNr: the number of the datastream event to be returned
        :return: A csv string with the data starting from event specified
        """
        header = self.build_header(
            org_id=org_id,
            aut_token=self.props.get_auth_token(cluster=self.cluster)
        )
        params = {'fromSequenceNr': sequenceNr}
        response = self.session.get(
            self.datastream_download_events.format(dataset_id),
            params=params,
            headers=header
        )

        if response.status_code in self.OK:
            return response.text

        try:
            msg = json.loads(response.content)
            raise Exception(msg)
        except json.JSONDecodeError:
            raise Exception(str(response.content))

    @single_org
    def create_command(self, org_id=None, *,
                       schema: dict,
                       name: str,
                       facets: list,
                       description: str,
                       cause: list,
                       dataset_uuid=None,
                       is_stream: bool = False):
        """

        :param org_id: organization id
        :type org_id: str
        :param schema: dataset schema
        :type schema: dict
        :param name: datatset name
        :type name: str
        :param facets: labels to be include don the dataset
        :type facets: list
        :param description: Description of the dataset
        :type description: str
        :param cause: The reason for this command
        :type cause: list
        :param dataset_uuid: Override of the dataset id
        :type dataset_uuid: str
        :param is_stream: decides if the created dataset is a stream dataset
        :type is_stream: bool
        :return: server response from the server
        """

        body = {
            "commands": [
                self.single_create_command(
                    schema=schema,
                    org_id=org_id,
                    name=name,
                    is_stream=is_stream,
                    facets=facets,
                    description=description,
                    cause=cause)
            ]
        }

        data_set_id = dataset_uuid if dataset_uuid is not None else str(uuid.uuid4())

        try:

            response = self._commit_dataset_command(org_id=org_id, data_set_id=data_set_id, command=body)

            response["uuid"] = data_set_id

            return response

        except Exception as es:
            raise Exception(es)

    def single_append_command(self, group_id, name):

        return {"$type": "append", "name": name, "group": group_id, "cause": []}

    def single_overwrite_command(self, group_id, name):
        return {"$type": "overwrite", "name": name, "group": group_id, "cause": []}

    def single_create_command(self, schema, org_id, name, is_stream, facets, description, cause):
        return {
            "$type": "create",
            "schema": schema,
            "org": org_id,
            "name": name,
            "isBounded": not is_stream,
            "facets": facets,
            "description": description,
            "cause": cause
        }
