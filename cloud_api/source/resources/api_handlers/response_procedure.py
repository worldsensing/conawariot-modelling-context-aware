from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models.ResponseProcedure import ResponseProcedure
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ResponseProcedureValidator

response_procedure_parser = reqparse.RequestParser()
response_procedure_parser.add_argument("name", type=str)
response_procedure_parser.add_argument("context_aware_rule_name", type=str)
response_procedure_parser.add_argument("procedure_type_name", type=str)
response_procedure_parser.add_argument("actuator_name", type=str)


class ResponseProcedureHandler:
    class ResponseProcedures(Resource):
        def get(self):
            logger.debug("[GET] /response_procedure-rules/")
            response = self.repository.response_procedure_repository. \
                get_all_response_procedures()

            return Response.success(
                [translator.response_procedure_translator(response_procedure)
                 for response_procedure in response])

        def post(self):
            logger.debug("[POST] /response_procedure-rules/")
            args = response_procedure_parser.parse_args()

            # Get ResponseProcedure arguments
            if ResponseProcedureValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.response_procedure_repository. \
                    get_response_procedure(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ResponseProcedureValidator \
                    .is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]

                response = self.repository.context_aware_rule_repository. \
                    get_context_aware_rule(context_aware_rule_name)
                if not response:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ResponseProcedureValidator.is_procedure_type_name_valid(args["procedure_type_name"]):
                procedure_type_name = args["procedure_type_name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ResponseProcedureValidator.is_actuator_name_valid(args["actuator_name"]):
                actuator_name = args["actuator_name"]

                response = self.repository.actuator_repository.get_actuator(actuator_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            response_procedure = ResponseProcedure(
                name=name,
                context_aware_rule_name=context_aware_rule_name,
                procedure_type_name=procedure_type_name,
                actuator_name=actuator_name,
            )

            result = self.repository.response_procedure_repository. \
                add_response_procedure(response_procedure)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class ResponseProcedure(Resource):
        def get(self, response_procedure_name):
            logger.debug(f"[GET] /response_procedure-rules/{response_procedure_name}")
            response = self.repository.response_procedure_repository. \
                get_response_procedure(response_procedure_name)

            if response:
                return Response.success(translator.response_procedure_translator(response))
            return Response.error(NOT_EXISTS_ID)

        # TODO To finish implementation
        def put(self, response_procedure_name):
            logger.debug(f"[PUT] /response_procedure-rules/{response_procedure_name}")
            args = response_procedure_parser.parse_args()

            response = self.repository.response_procedure_repository. \
                get_response_procedure(response_procedure_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get ResponseProcedure arguments
            if ResponseProcedureValidator \
                    .is_context_aware_rule_name_valid(args["context_aware_name"]):
                context_aware_name = args["context_aware_name"]
            else:
                context_aware_name = None

            response_procedure = {
                "name": response_procedure_name,
                "context_aware_name": context_aware_name,
            }

            response = self.repository.response_procedure_repository. \
                update_response_procedure(response_procedure_name,
                                          response_procedure)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, response_procedure_name):
            logger.debug(f"[DELETE] /response_procedure-rules/{response_procedure_name}")
            response = self.repository.response_procedure_repository.get_response_procedure(
                response_procedure_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.response_procedure_repository.delete_response_procedure(
                response_procedure_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
