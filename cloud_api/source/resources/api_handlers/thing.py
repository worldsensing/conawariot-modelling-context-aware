from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, NOT_THING_TYPE, \
    EXISTS_ID, NOT_EXISTS_LOCATION
from models import Thing
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ThingValidator

thing_parser = reqparse.RequestParser()
thing_parser.add_argument("name", type=str)
thing_parser.add_argument("type_name", type=str)
thing_parser.add_argument("location_name", type=str, required=False)


class ThingHandler:
    class Things(Resource):
        def get(self):
            logger.debug(f"[GET] /things/")
            response = self.repository.thing_repository.get_all_things()

            return Response.success(
                [translator.thing_translator(thing) for thing in response])

        def post(self):
            logger.debug(f"[POST] /things/")
            args = thing_parser.parse_args()

            # Get Thing arguments
            if ThingValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.thing_repository.get_thing(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ThingValidator.is_type_name_valid(args["type_name"]):
                thing_type_name = args["type_name"]

                response = self.repository.thing_type_repository.get_thing_type(thing_type_name)
                if response is None:
                    return Response.error(NOT_THING_TYPE)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ThingValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(location_name)
                if response is None:
                    return Response.error(NOT_EXISTS_LOCATION)
            else:
                location_name = None

            thing = Thing(name=name, type_name=thing_type_name, location_name=location_name)

            result = self.repository.thing_repository.add_thing(thing)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class Thing(Resource):
        def get(self, thing_name):
            logger.debug(f"[GET] /things/{thing_name}")
            response = self.repository.thing_repository.get_thing(thing_name)

            if response:
                return Response.success(translator.thing_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, thing_name):
            logger.debug(f"[PUT] /things/{thing_name}")
            args = thing_parser.parse_args()

            response = self.repository.thing_repository.get_thing(thing_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get Thing arguments
            if ThingValidator.is_name_valid(args["name"]):
                name = args["name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ThingValidator.is_type_name_valid(args["type_name"]):
                type_name = args["type_name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ThingValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            thing = {
                "name": name,
                "type_name": type_name,
                "location_name": location_name
            }

            response = self.repository.thing_repository.update_thing(thing_name, thing)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, thing_name):
            logger.debug(f"[DELETE] /things/{thing_name}")
            response = self.repository.thing_repository.get_thing(thing_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.thing_repository.delete_thing(thing_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)

    class ThingObservation(Resource):
        def get(self, thing_name):
            logger.debug(f"[GET] UNUSED")
            response = self.repository.thing_repository.get_thing(thing_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            response = self.repository.thing_repository.get_observations_filter_thing(thing_name)

            return Response.success(
                [translator.observation_translator(observation) for observation in response])
