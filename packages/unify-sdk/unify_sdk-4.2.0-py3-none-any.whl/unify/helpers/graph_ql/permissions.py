import json
from unify.helpers.graph_ql.graphql import GraphQLBuilder
from unify.helpers.Permissions import ArtifactType
from unify.helpers.Permissions import Verbs, Domains, Effects


class PermissionsGraphQl(GraphQLBuilder):

    def __init__(self):
        pass

    def build_get_org_config_query(self):
        return self.build_generic_query(
            query_name="permissions",
            operation_type="query",
            fields=[self.build_simple_query(
                query_name="getOrgConfig",
                fields=["orgId", "globalRuleOptOut"]
            )]
        )

    def get_org_config(self, ):
        return self.build_response(
            query=self.build_get_org_config_query()
        )

    def build_user_selector(self):
        return self.build_generic_query(
            query_name="userSelector", fields=["id", "selectorType", "org", "displayName", "selector"]
        )

    def build_resource_selector(self):
        return self.build_generic_query(
            query_name="resourceSelector",
            fields=["id", "selectorType", "org", "displayName", "selector"]
        )

    def build_get_rules_query(self):
        return self.build_generic_query(
            query_name="permissions",
            operation_type="query",
            fields=[self.build_simple_query(
                query_name="getRules",
                fields=[
                    "id", "domains", "scope", "verb", "effect",
                    self.build_user_selector(),
                    self.build_resource_selector()
                ]
            )]
        )

    def get_rules(self):
        return self.build_response(
            query=self.build_get_rules_query(),
        )

    def build_get_user_rules_query(self, user_id):
        queries = [
            self.build_simple_query(
                query_name="getUserRules",
                fields=[
                    "id", "scope", "effect", "verb", "domains",
                    self.build_user_selector(),
                    self.build_resource_selector()
                ],
                query_input={"userId": user_id}
            )
        ]

        return self.build_generic_query(
            query_name="permissions",
            operation_type="query",
            fields=queries,
        )

    def get_user_rules(self, user_id):
        return self.build_response(
            query=self.build_get_user_rules_query(user_id),
            variables={"userId": user_id}
        )

    def build_artifact_rules_query(self, artifact_type, artifact_id):
        queries = [
            self.build_simple_query(
                query_name="getArtifactRules",
                fields=[
                    "id", "scope", "effect", "verb", "domains",
                    self.build_user_selector(),
                    self.build_resource_selector()
                ],
                query_input={"artifactId": '"{}"'.format(str(artifact_id)), "at": artifact_type}
            )
        ]

        return self.build_generic_query(
            query_name="permissions",
            operation_type="query",
            fields=queries,
        )

    def get_artifact_rules(self, artifact_type, artifact_id):
        return self.build_response(
            query=self.build_artifact_rules_query(artifact_type, artifact_id),
        )

    def build_selector_definitions_query(self):
        return self.build_generic_query(
            query_name="permissions",
            operation_type="query",
            fields=[self.build_simple_query(
                query_name="getSelectorDefinitions",
                fields=[
                    "id", "org", "displayName", "selectorType", "selector"
                ]
            )]
        )

    def get_selector_definitions(self):
        return self.build_response(
            query=self.build_selector_definitions_query()
        )

    def build_check_query(self, artifact_type, artifact_id, user_id, verb):
        queries = [
            self.build_simple_query(
                query_name="check",
                fields=[
                    "allowed"
                ],
                query_input={
                    "artifactId": '"{}"'.format(str(artifact_id)),
                    "at": artifact_type,
                    "userId": user_id,
                    "verb": verb
                }
            )
        ]
        return self.build_generic_query(
            query_name="permissions",
            operation_type="query",
            fields=queries,
        )

    def check(self, artifact_type, artifact_id, user_id, verb):
        return self.build_response(
            query=self.build_check_query(artifact_type, artifact_id, user_id, verb)
        )

    def build_selector_definition_query(self, selector_id):
        queries = [
            self.build_simple_query(
                query_name="getSelectorDefinition",
                fields=[
                    "id", "org", "displayName", "selectorType", "selector"
                ],
                query_input={"id": selector_id}
            )
        ]

        return self.build_generic_query(
            query_name="permissions",
            operation_type="query",
            fields=queries,
        )

    def get_selector_definition(self, selector_id):
        return self.build_response(
            query=self.build_selector_definition_query(selector_id=selector_id)
        )

    def build_response(self, query, variables: dict = None, operation_name=None):
        obj = {
            "query": query
        }

        if operation_name:
            obj["operation_name"] = operation_name

        if variables:
            obj["variables"] = variables

        return json.dumps(obj)

    def build_rule_mutation(self, domain, verb, effect, userSelector, resourceSelector):
        sub_data = {
            "domains": domain,
            "verb": verb,
            "effect": effect,
            "userSelector": userSelector,
            "resourceSelector": resourceSelector
        }

        final = []

        for key, value in sub_data.items():
            final.append("{}:{}".format(key, value))

        data = {
            "rule": "{" + ' '.join(final) + "}"
        }

        simple = self.build_simple_query(
            query_name="addRule",
            query_input=data,
        )

        return self.build_response(
            query="mutation { permissions { " + simple + "}}"
        )

    def build_delete_rule_mutation(self, rule_id):

        simple = self.build_simple_query(
            query_name="deleteRule",
            query_input={"id": '"{}"'.format(rule_id)},
        )

        return self.build_response(
            query="mutation { permissions { " + simple + "}}"
        )


    def build_add_selector_mutation(self, domain, verb, effect, userSelector, resourceSelector):
        sub_data = {
            "domains": domain,
            "verb": verb,
            "effect": effect,
            "userSelector": userSelector,
            "resourceSelector": resourceSelector
        }

        final = []

        for key, value in sub_data.items():
            final.append("{}:{}".format(key, value))

        data = {
            "rule": "{" + ' '.join(final) + "}"
        }

        simple = self.build_simple_query(
            query_name="addRule",
            query_input=data,
        )

        return self.build_response(
            query="mutation { permissions { " + simple + "}}"
        )
