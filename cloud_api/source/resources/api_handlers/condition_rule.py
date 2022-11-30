from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models.ConditionRule import ConditionRule
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ConditionRuleValidator

condition_rule_parser = reqparse.RequestParser()
condition_rule_parser.add_argument("name", type=str)
condition_rule_parser.add_argument("context_aware_rule_name", type=str)
condition_rule_parser.add_argument("event_rule_1_name", type=str, required=False)
condition_rule_parser.add_argument("event_rule_2_name", type=str, required=False)
condition_rule_parser.add_argument("condition_rule_1_name", type=str, required=False)
condition_rule_parser.add_argument("condition_rule_2_name", type=str, required=False)
condition_rule_parser.add_argument("condition_comparation_type", type=str)


class ConditionRuleHandler:
    class ConditionRules(Resource):
        def get(self):
            logger.debug("[GET] /condition-rules/")
            response = self.repository.condition_rule_repository. \
                get_all_condition_rules()

            return Response.success(
                [translator.condition_rule_translator(condition_rule)
                 for condition_rule in response])

        def post(self):
            logger.debug("[POST] /condition-rules/")
            args = condition_rule_parser.parse_args()

            # Get ConditionRule arguments
            if ConditionRuleValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.condition_rule_repository. \
                    get_condition_rule(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ConditionRuleValidator \
                    .is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]

                response = self.repository.context_aware_rule_repository. \
                    get_context_aware_rule(context_aware_rule_name)
                if not response:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            event_rule_1_name = None
            if ConditionRuleValidator.is_event_rule_name_valid(args["event_rule_1_name"]):
                event_rule_1_name = args["event_rule_1_name"]

                response = self.repository.event_rule_repository.get_event_rule(event_rule_1_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)

            event_rule_2_name = None
            if ConditionRuleValidator.is_event_rule_name_valid(args["event_rule_2_name"]):
                event_rule_2_name = args["event_rule_2_name"]

                response = self.repository.event_rule_repository.get_event_rule(event_rule_2_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)

            condition_rule_1_name = None
            if ConditionRuleValidator.is_name_valid(args["condition_rule_1_name"]):
                condition_rule_1_name = args["condition_rule_1_name"]

                response = self.repository.condition_rule_repository. \
                    get_condition_rule(condition_rule_1_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)

            condition_rule_2_name = None
            if ConditionRuleValidator.is_name_valid(args["condition_rule_2_name"]):
                condition_rule_2_name = args["condition_rule_2_name"]

                response = self.repository.condition_rule_repository. \
                    get_condition_rule(condition_rule_2_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)

            if ConditionRuleValidator. \
                    is_condition_comparation_type_valid(args["condition_comparation_type"]):
                condition_comparation_type = args["condition_comparation_type"]
            else:
                return Response.error(FIELD_NOT_VALID)

            condition_rule = ConditionRule(
                name=name,
                context_aware_rule_name=context_aware_rule_name,
                event_rule_1_name=event_rule_1_name,
                event_rule_2_name=event_rule_2_name,
                condition_rule_1_name=condition_rule_1_name,
                condition_rule_2_name=condition_rule_2_name,
                condition_comparation_type=condition_comparation_type,
            )

            result = self.repository.condition_rule_repository. \
                add_condition_rule(condition_rule)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class ConditionRule(Resource):
        def get(self, condition_rule_name):
            logger.debug(f"[GET] /condition-rules/{condition_rule_name}")
            response = self.repository.condition_rule_repository. \
                get_condition_rule(condition_rule_name)

            if response:
                return Response.success(translator.condition_rule_translator(response))
            return Response.error(NOT_EXISTS_ID)

        # TODO To finish implementation
        def put(self, condition_rule_name):
            logger.debug(f"[PUT] /condition-rules/{condition_rule_name}")
            args = condition_rule_parser.parse_args()

            response = self.repository.condition_rule_repository. \
                get_condition_rule(condition_rule_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get ConditionRule arguments
            if ConditionRuleValidator \
                    .is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]
            else:
                context_aware_rule_name = None

            condition_rule = {
                "name": condition_rule_name,
                "context_aware_rule_name": context_aware_rule_name,
            }

            response = self.repository.condition_rule_repository. \
                update_condition_rule(condition_rule_name, condition_rule)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, condition_rule_name):
            logger.debug(f"[DELETE] /condition-rules/{condition_rule_name}")
            response = self.repository.condition_rule_repository.get_condition_rule(
                condition_rule_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.condition_rule_repository.delete_condition_rule(
                condition_rule_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
