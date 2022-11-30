from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models import ContextAwareRule
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ContextAwareRuleValidator

context_aware_rule_parser = reqparse.RequestParser()
context_aware_rule_parser.add_argument("name", type=str)
context_aware_rule_parser.add_argument("executing", type=bool, required=False)


class ContextAwareRulesHandler:
    class ContextAwareRules(Resource):
        def get(self):
            logger.debug("[GET] /context-aware-rules/")
            response = self.repository.context_aware_rule_repository. \
                get_all_context_aware_rules()

            return Response.success(
                [translator.context_aware_rule_translator(context_aware_rule)
                 for context_aware_rule in response])

        def post(self):
            logger.debug("[POST] /context-aware-rules/")
            args = context_aware_rule_parser.parse_args()

            # Get ContextAwareRule arguments
            if ContextAwareRuleValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.context_aware_rule_repository. \
                    get_context_aware_rule(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ContextAwareRuleValidator.is_executing_valid(args["executing"]):
                executing = args["executing"]
            else:
                executing = True

            context_aware_rule = ContextAwareRule(
                name=name,
                executing=executing,
            )

            result = self.repository.context_aware_rule_repository. \
                add_context_aware_rule(context_aware_rule)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class ContextAwareRule(Resource):
        def get(self, context_aware_rule_name):
            logger.debug(f"[GET] /context-aware-rules/{context_aware_rule_name}")
            response = self.repository.context_aware_rule_repository. \
                get_context_aware_rule(context_aware_rule_name)

            if response:
                return Response.success(translator.context_aware_rule_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, context_aware_rule_name):
            logger.debug(f"[PUT] /context-aware-rules/{context_aware_rule_name}")
            args = context_aware_rule_parser.parse_args()

            response = self.repository.context_aware_rule_repository. \
                get_context_aware_rule(context_aware_rule_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get ContextAwareRule arguments
            if ContextAwareRuleValidator.is_executing_valid(args["executing"]):
                executing = args["executing"]
            else:
                executing = True

            context_aware_rule = {
                "name": context_aware_rule_name,
                "executing": executing,
            }

            response = self.repository.context_aware_rule_repository. \
                update_context_aware_rule(context_aware_rule_name, context_aware_rule)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, context_aware_rule_name):
            logger.debug(f"[DELETE] /context-aware-rules/{context_aware_rule_name}")
            response = self.repository.context_aware_rule_repository.get_context_aware_rule(
                context_aware_rule_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.context_aware_rule_repository.delete_context_aware_rule(
                context_aware_rule_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)

    class ContextAwareRulesComponents(Resource):
        def get(self, context_aware_rule_name):
            logger.debug(f"[GET] /context-aware-rules/{context_aware_rule_name}/components")
            response = self.repository.context_aware_rule_repository. \
                get_context_aware_rule(context_aware_rule_name)

            if response:
                return Response.success(
                    translator.context_aware_rule_components_translator(response))
            return Response.error(NOT_EXISTS_ID)
