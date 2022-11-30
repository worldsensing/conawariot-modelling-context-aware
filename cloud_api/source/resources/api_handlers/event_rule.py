from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models.EventRule import EventRule
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import EventRuleValidator

event_rule_parser = reqparse.RequestParser()
event_rule_parser.add_argument("name", type=str)
event_rule_parser.add_argument("context_aware_rule_name", type=str)
event_rule_parser.add_argument("event_rule_type_name", type=str, required=False)
event_rule_parser.add_argument("sensor_1_name", type=str, required=False)
event_rule_parser.add_argument("sensor_2_name", type=str, required=False)
event_rule_parser.add_argument("value_to_compare_boolean", type=bool, required=False)
event_rule_parser.add_argument("value_to_compare_string", type=str, required=False)
event_rule_parser.add_argument("value_to_compare_integer", type=int, required=False)
event_rule_parser.add_argument("value_to_compare_float", type=float, required=False)


class EventRuleHandler:
    class EventRules(Resource):
        def get(self):
            logger.debug("[GET] /event-rules/")
            response = self.repository.event_rule_repository. \
                get_all_event_rules()

            return Response.success(
                [translator.event_rule_translator(event_rule)
                 for event_rule in response])

        def post(self):
            logger.debug("[POST] /event-rules/")
            args = event_rule_parser.parse_args()

            # Get EventRule arguments
            if EventRuleValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.event_rule_repository. \
                    get_event_rule(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if EventRuleValidator \
                    .is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]

                response = self.repository.context_aware_rule_repository. \
                    get_context_aware_rule(context_aware_rule_name)
                if not response:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if EventRuleValidator.is_event_rule_type_name_valid(args["event_rule_type_name"]):
                event_rule_type_name = args["event_rule_type_name"]

                response = self.repository.event_rule_type_repository. \
                    get_event_rule_type(event_rule_type_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if EventRuleValidator.is_sensor_name_valid(args["sensor_1_name"]):
                sensor_1_name = args["sensor_1_name"]

                response = self.repository.sensor_repository.get_sensor(sensor_1_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            sensor_2_name = None
            if EventRuleValidator.is_sensor_name_valid(args["sensor_2_name"]):
                sensor_2_name = args["sensor_2_name"]

                response = self.repository.sensor_repository.get_sensor(sensor_2_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)

            value_to_compare_boolean = None
            if EventRuleValidator \
                    .is_value_to_compare_boolean_valid(args["value_to_compare_boolean"]):
                value_to_compare_boolean = args["value_to_compare_boolean"]

            value_to_compare_string = None
            if EventRuleValidator.is_value_to_compare_string_valid(args["value_to_compare_string"]):
                value_to_compare_string = args["value_to_compare_string"]

            value_to_compare_integer = None
            if EventRuleValidator. \
                    is_value_to_compare_integer_valid(args["value_to_compare_integer"]):
                value_to_compare_integer = args["value_to_compare_integer"]

            value_to_compare_float = None
            if EventRuleValidator.is_value_to_compare_float_valid(args["value_to_compare_float"]):
                value_to_compare_float = args["value_to_compare_float"]

            event_rule = EventRule(
                name=name,
                context_aware_rule_name=context_aware_rule_name,
                event_rule_type_name=event_rule_type_name,
                sensor_1_name=sensor_1_name,
                sensor_2_name=sensor_2_name,
                value_to_compare_boolean=value_to_compare_boolean,
                value_to_compare_string=value_to_compare_string,
                value_to_compare_integer=value_to_compare_integer,
                value_to_compare_float=value_to_compare_float,
            )

            result = self.repository.event_rule_repository.add_event_rule(event_rule)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class EventRule(Resource):
        def get(self, event_rule_name):
            logger.debug(f"[GET] /event-rules/{event_rule_name}")
            response = self.repository.event_rule_repository. \
                get_event_rule(event_rule_name)

            if response:
                return Response.success(translator.event_rule_translator(response))
            return Response.error(NOT_EXISTS_ID)

        # TODO To finish implementation
        def put(self, event_rule_name):
            logger.debug(f"[PUT] /event-rules/{event_rule_name}")
            args = event_rule_parser.parse_args()

            response = self.repository.event_rule_repository. \
                get_event_rule(event_rule_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get EventRule arguments
            if EventRuleValidator \
                    .is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]
            else:
                context_aware_rule_name = None

            event_rule = {
                "name": event_rule_name,
                "context_aware_rule_name": context_aware_rule_name,
            }

            response = self.repository.event_rule_repository. \
                update_event_rule(event_rule_name, event_rule)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, event_rule_name):
            logger.debug(f"[DELETE] /event-rules/{event_rule_name}")
            response = self.repository.event_rule_repository.get_event_rule(
                event_rule_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.event_rule_repository.delete_event_rule(
                event_rule_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
