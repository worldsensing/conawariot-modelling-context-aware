from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID, \
    NOT_EXISTS_LOCATION
from models import Actuator
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ActuatorValidator

actuator_parser = reqparse.RequestParser()
actuator_parser.add_argument("thing_name", type=str)
actuator_parser.add_argument("name", type=str)
actuator_parser.add_argument("actuatable_property_name", type=str)
actuator_parser.add_argument("location_name", type=str)


class ActuatorHandler:
    class Actuators(Resource):
        def get(self):
            logger.debug(f"[GET] /actuators/")
            response = self.repository.actuator_repository.get_all_actuators()

            return Response.success(
                [translator.actuator_translator(actuator) for actuator in response])

        def post(self):
            logger.debug(f"[POST] /actuators/")
            args = actuator_parser.parse_args()

            # Get Actuator arguments
            if ActuatorValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.actuator_repository.get_actuator(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuatorValidator.is_thing_name_valid(args["thing_name"]):
                thing_name = args["thing_name"]

                response = self.repository.thing_repository.get_thing(thing_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuatorValidator. \
                    is_actuatable_property_name_valid(args["actuatable_property_name"]):
                actuatable_property_name = args["actuatable_property_name"]

                response = self.repository.actuatable_property_repository. \
                    get_actuatable_property(actuatable_property_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuatorValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(location_name)
                if response is None:
                    return Response.error(NOT_EXISTS_LOCATION)
            else:
                location_name = None

            actuator = Actuator(
                name=name,
                thing_name=thing_name,
                actuatable_property_name=actuatable_property_name,
                location_name=location_name)

            result = self.repository.actuator_repository.add_actuator(actuator)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class Actuator(Resource):
        def get(self, actuator_name):
            logger.debug(f"[GET] /actuators/{actuator_name}")
            response = self.repository.actuator_repository.get_actuator(actuator_name)

            if response:
                return Response.success(translator.actuator_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, actuator_name):
            logger.debug(f"[PUT] /actuators/{actuator_name}")
            args = actuator_parser.parse_args()

            response = self.repository.actuator_repository.get_actuator(actuator_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get Actuator arguments
            if ActuatorValidator.is_thing_name_valid(args["thing_name"]):
                thing_name = args["thing_name"]

                response = self.repository.thing_repository.get_thing(thing_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuatorValidator. \
                    is_actuatable_property_name_valid(args["actuatable_property_name"]):
                actuatable_property_name = args["actuatable_property_name"]

                response = self.repository.actuatable_property_repository. \
                    get_actuatable_property(actuatable_property_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuatorValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(location_name)
                if response is None:
                    return Response.error(NOT_EXISTS_LOCATION)
            else:
                location_name = None

            actuator = {
                "name": actuator_name,
                "thing_name": thing_name,
                "actuatable_property_name": actuatable_property_name,
                "location_name": location_name,
            }

            response = self.repository.actuator_repository.update_actuator(actuator_name, actuator)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, actuator_name):
            logger.debug(f"[DELETE] /actuators/{actuator_name}")
            response = self.repository.actuator_repository.get_actuator(actuator_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.actuator_repository.delete_actuator(actuator_name)

            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)
