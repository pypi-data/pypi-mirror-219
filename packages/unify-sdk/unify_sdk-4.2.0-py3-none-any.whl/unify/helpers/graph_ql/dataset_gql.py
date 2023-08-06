import json

from unify.helpers.graph_ql.graphql import GraphQLBuilder


class DatasetGrapql(GraphQLBuilder):

    def build_dataset_query(
            self,
            include_schema=True,
            count=True,
            page_num=1,
            page_size=100,
            is_deleted=False,
            facets=None,
            other_filters: dict = None
    ):

        art_count = self.build_generic_query(
            query_name="artifactCount",
            query_input={"pagination": "$pagination"},
        )

        artifacts = self.build_artifacts_query(pipeline=False)

        common_parts = self.build_common_parts_fragment()

        LastUpdatedParts = self.build_last_updated_fragment()

        fields = [
            "table",
            "numPipelines",
            "latestSequenceNumber",
            self.build_simple_query(
                query_name="labels",
                fields=[
                    'raw(fields: ["ean_source_type", "ean_ready", "ean_dataArchiveServerName"])',
                    "__typename"
                ]
            ),
            "__typename"
        ]

        if include_schema:
            fields.append("schema")

        DatasetParts = self.build_fragment(
            fragment_name="DatasetParts",
            interface_name="Dataset",
            fields=fields
        )

        queries = [artifacts]

        if count:
            queries.append(art_count)

        final = self.build_generic_query(
            operation_name="fetchDatasets",
            operation_type="query",
            operation_input={"$pagination": "PaginationInput!"},
            operation_queries=queries
        )

        final_query = "".join(
            [common_parts, LastUpdatedParts, DatasetParts, final]
        )

        filters = 'isDeleted = "{}" && type = "dataset"'.format(is_deleted)

        if facets:
            for facet in facets:
                filters += ' && facets = "{}"'.format(str(facet))

        if other_filters:
            for key_filter, value_filter in other_filters.items():
                filters += ' && ({} ~ \"{}\")'.format(key_filter, value_filter)

        results = {
            "operationName": "fetchDatasets",
            "query": final_query,
            "variables": {
                "pagination": {
                    "pageInfo": {
                        "pageNum": page_num,
                        "pageSize": page_size
                    },
                    "filter": filters
                }
            }
        }

        return json.dumps(results)
