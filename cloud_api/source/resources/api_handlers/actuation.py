from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID
from models import Actuation
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ActuationValidator

actuation_parser = reqparse.RequestParser()
actuation_parser.add_argument("observation_id", type=int)
actuation_parser.add_argument("context_aware_rule_name", type=str)
actuation_parser.add_argument("time_start", type=str)
actuation_parser.add_argument("time_end", type=str, required=False)


class ActuationHandler:
    class Actuations(Resource):
        def get(self):
            logger.debug(f"[GET] /actuations/")
            response = self.repository.actuation_repository.get_all_actuations()

            return Response.success(
                [translator.actuation_translator(actuation) for
                 actuation in response])

        def post(self):
            logger.debug(f"[POST] /actuations/")
            args = actuation_parser.parse_args()

            # Get Actuation arguments
            if ActuationValidator.is_observation_id_valid(args["observation_id"]):
                observation_id = args["observation_id"]

                observation = self.repository.observation_repository.get_observation(observation_id)
                if not observation:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuationValidator. \
                    is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]

                context_aware_rule = self.repository.context_aware_rule_repository. \
                    get_context_aware_rule(context_aware_rule_name)
                if not context_aware_rule:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuationValidator.is_time_start_valid(args["time_start"]):
                time_start = args["time_start"]
            else:
                time_start = None

            if ActuationValidator.is_time_end_valid(args["time_end"]):
                time_end = args["time_end"]
            else:
                time_end = None

            actuation = Actuation(observation_id=observation_id,
                                  context_aware_rule_name=context_aware_rule_name,
                                  time_start=time_start,
                                  time_end=time_end)

            result = self.repository.actuation_repository.add_actuation(actuation)
            if result:
                return Response.success({"id": result})

            return Response.error(GENERIC)

    class Actuation(Resource):
        def get(self, actuation_id):
            logger.debug(f"[GET] /actuations/{actuation_id}")
            response = self.repository.actuation_repository.get_actuation(actuation_id)

            if response:
                return Response.success(translator.actuation_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def patch(self, actuation_id):
            logger.debug(f"[PATCH] /actuations/{actuation_id}")
            args = actuation_parser.parse_args()

            actuation = self.repository.actuation_repository.get_actuation(actuation_id)
            if actuation is None:
                return Response.error(NOT_EXISTS_ID)

            # Get Actuation arguments
            if ActuationValidator.is_observation_id_valid(args["observation_id"]):
                observation_id = args["observation_id"]

                observation = self.repository.observation_repository.get_observation(observation_id)
                if not observation:
                    return Response.error(NOT_EXISTS_ID)
            else:
                observation_id = actuation.observation_id

            if ActuationValidator. \
                    is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]

                context_aware_rule = self.repository.context_aware_rule_repository. \
                    get_context_aware_rule(context_aware_rule_name)
                if not context_aware_rule:
                    return Response.error(NOT_EXISTS_ID)
            else:
                context_aware_rule_name = actuation.context_aware_rule_name

            if ActuationValidator.is_time_start_valid(args["time_start"]):
                time_start = args["time_start"]
            else:
                time_start = actuation.time_start

            if ActuationValidator.is_time_end_valid(args["time_end"]):
                time_end = args["time_end"]
            else:
                time_end = actuation.time_end

            actuation = {
                "observation_id": observation_id,
                "context_aware_rule_name": context_aware_rule_name,
                "time_start": time_start,
                "time_end": time_end
            }

            actuation = self.repository.actuation_repository.update_actuation(actuation_id,
                                                                              actuation)
            if actuation:
                return Response.success({"id": actuation})

            return Response.error(GENERIC)

        def put(self, actuation_id):
            logger.debug(f"[PUT] /actuations/{actuation_id}")
            args = actuation_parser.parse_args()

            response = self.repository.actuation_repository.get_actuation(actuation_id)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get Actuation arguments
            if ActuationValidator.is_observation_id_valid(args["observation_id"]):
                observation_id = args["observation_id"]

                observation = self.repository.observation_repository.get_observation(observation_id)
                if not observation:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuationValidator. \
                    is_context_aware_rule_name_valid(args["context_aware_rule_name"]):
                context_aware_rule_name = args["context_aware_rule_name"]

                context_aware_rule = self.repository.context_aware_rule_repository. \
                    get_context_aware_rule(context_aware_rule_name)
                if not context_aware_rule:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuationValidator.is_time_start_valid(args["time_start"]):
                time_start = args["time_start"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuationValidator.is_time_end_valid(args["time_end"]):
                time_end = args["time_end"]
            else:
                time_end = None

            actuation = {
                "observation_id": observation_id,
                "context_aware_rule_name": context_aware_rule_name,
                "time_start": time_start,
                "time_end": time_end
            }

            response = self.repository.actuation_repository.update_actuation(actuation_id,
                                                                             actuation)
            if response:
                return Response.success({"id": response})

            return Response.error(GENERIC)

        def delete(self, actuation_id):
            logger.debug(f"[DELETE] /actuations/{actuation_id}")
            response = self.repository.actuation_repository.get_actuation(actuation_id)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.actuation_repository.delete_actuation(actuation_id)
            if result:
                return Response.success({"id": result})
            return Response.error(GENERIC)
