from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, THING_TYPE_HAS_TYPE, \
    EXISTS_ID
from models import ThingType
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ThingTypeValidator

thing_type_parser = reqparse.RequestParser()
thing_type_parser.add_argument("name", type=str)


class ThingTypeHandler:
    class ThingTypes(Resource):
        def get(self):
            logger.debug(f"[GET] /thing-types/")
            response = self.repository.thing_type_repository.get_all_thing_types()

            return Response.success(
                [translator.thing_type_translator(thing_type)
                 for thing_type in response])

        def post(self):
            logger.debug(f"[POST] /thing-types/")
            args = thing_type_parser.parse_args()

            # Get ThingType arguments
            if ThingTypeValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.thing_type_repository.get_thing_type(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            thing_type = ThingType(name=name)

            result = self.repository.thing_type_repository.add_thing_type(thing_type)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class ThingType(Resource):
        def get(self, thing_type_name):
            logger.debug(f"[GET] /thing-types/{thing_type_name}")
            response = self.repository.thing_type_repository.get_thing_type(thing_type_name)

            if response:
                return Response.success(translator.thing_type_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, thing_type_name):
            logger.debug(f"[PUT] /thing-types/{thing_type_name}")
            args = thing_type_parser.parse_args()

            response = self.repository.thing_type_repository.get_thing_type(thing_type_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get ThingType arguments
            if ThingTypeValidator.is_name_valid(args["name"]):
                name = args["name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            thing = {
                "name": name,
            }

            response = self.repository.thing_type_repository.update_thing_type(thing_type_name,
                                                                               thing)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, thing_type_name):
            logger.debug(f"[DELETE] /thing-types/{thing_type_name}")
            response = self.repository.thing_type_repository.get_thing_type(thing_type_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            response = self.repository.thing_repository.get_things_filter_thing_type(
                thing_type_name)
            if response:
                return Response.error(THING_TYPE_HAS_TYPE)

            result = self.repository.thing_type_repository.delete_thing_type(thing_type_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
