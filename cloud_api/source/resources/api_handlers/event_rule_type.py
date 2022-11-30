from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models.EventRuleType import EventRuleType
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import EventRuleTypeValidator

event_rule_type_parser = reqparse.RequestParser()
event_rule_type_parser.add_argument("name", type=str)
event_rule_type_parser.add_argument("event_rule_type", type=str)
event_rule_type_parser.add_argument("event_rule_comparation_type", type=str, required=False)
event_rule_type_parser.add_argument("event_rule_value_type", type=str, required=False)


class EventRuleTypeHandler:
    class EventRuleTypes(Resource):
        def get(self):
            logger.debug("[GET] /event-rule-types/")
            response = self.repository.event_rule_type_repository. \
                get_all_event_rule_types()

            return Response.success(
                [translator.event_rule_type_translator(event_rule_type)
                 for event_rule_type in response])

        def post(self):
            logger.debug("[POST] /event-rule-types/")
            args = event_rule_type_parser.parse_args()

            # Get EventRuleType arguments
            if EventRuleTypeValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.event_rule_type_repository. \
                    get_event_rule_type(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if EventRuleTypeValidator \
                    .is_event_rule_type_valid(args["event_rule_type"]):
                event_rule_type = args["event_rule_type"]
            else:
                event_rule_type = None

            if EventRuleTypeValidator \
                    .is_event_rule_comparation_type_valid(args["event_rule_comparation_type"]):
                event_rule_comparation_type = args["event_rule_comparation_type"]
            else:
                event_rule_comparation_type = None

            if EventRuleTypeValidator \
                    .is_event_rule_value_type_valid(args["event_rule_value_type"]):
                event_rule_value_type = args["event_rule_value_type"]
            else:
                event_rule_value_type = None

            event_rule_type = EventRuleType(
                name=name,
                event_rule_type=event_rule_type,
                event_rule_comparation_type=event_rule_comparation_type,
                event_rule_value_type=event_rule_value_type,
            )

            result = self.repository.event_rule_type_repository. \
                add_event_rule_type(event_rule_type)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class EventRuleType(Resource):
        def get(self, event_rule_type_name):
            logger.debug(f"[GET] /event-rule-types/{event_rule_type_name}")
            response = self.repository.event_rule_type_repository. \
                get_event_rule_type(event_rule_type_name)

            if response:
                return Response.success(translator.event_rule_type_translator(response))
            return Response.error(NOT_EXISTS_ID)

        # TODO To finish implementation
        def put(self, event_rule_type_name):
            logger.debug(f"[PUT] /event-rules/{event_rule_type_name}")
            args = event_rule_type_parser.parse_args()

            response = self.repository.event_rule_type_repository. \
                get_event_rule_type(event_rule_type_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get EventRuleType arguments
            if EventRuleTypeValidator \
                    .is_event_rule_type_valid(args["event_rule_type"]):
                event_rule_type = args["event_rule_type"]
            else:
                event_rule_type = None

            if EventRuleTypeValidator \
                    .is_event_rule_comparation_type_valid(args["event_rule_comparation_type"]):
                event_rule_comparation_type = args["event_rule_comparation_type"]
            else:
                event_rule_comparation_type = None

            if EventRuleTypeValidator \
                    .is_event_rule_value_type_valid(args["event_rule_value_type"]):
                event_rule_value_type = args["event_rule_value_type"]
            else:
                event_rule_value_type = None

            event_rule_type = {
                "name": event_rule_type_name,
                "event_rule_type": event_rule_type,
                "event_rule_comparation_type": event_rule_comparation_type,
                "event_rule_value_type": event_rule_value_type,
            }

            response = self.repository.event_rule_type_repository. \
                update_event_rule_type(event_rule_type_name, event_rule_type)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, event_rule_type_name):
            logger.debug(f"[DELETE] /event-rule-types/{event_rule_type_name}")
            response = self.repository.event_rule_type_repository.get_event_rule_type(
                event_rule_type_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.event_rule_type_repository.delete_event_rule_type(
                event_rule_type_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
