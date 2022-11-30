from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models import Location
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import LocationValidator

location_parser = reqparse.RequestParser()
location_parser.add_argument("name", type=str)
location_parser.add_argument("latlng", type=str, required=False)


class LocationHandler:
    class Locations(Resource):
        def get(self):
            logger.debug(f"[GET] /locations/")
            response = self.repository.location_repository.get_all_locations()

            return Response.success(
                [translator.location_translator(location)
                 for location in response])

        def post(self):
            logger.debug(f"[POST] /locations/")
            args = location_parser.parse_args()

            # Get Location arguments
            if LocationValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.location_repository.get_location(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if LocationValidator.is_latlng_valid(args["latlng"]):
                latlng = args["latlng"]
            else:
                latlng = None

            location = Location(name=name, latlng=latlng)

            result = self.repository.location_repository.add_location(location)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class Location(Resource):
        def get(self, location_name):
            logger.debug(f"[GET] /locations/{location_name}")
            response = self.repository.location_repository.get_location(location_name)

            if response:
                return Response.success(translator.location_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, location_name):
            logger.debug(f"[PUT] /locations/{location_name}")
            args = location_parser.parse_args()

            # Get Location arguments
            if LocationValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.location_repository.get_location(name)
                if response is None:
                    return Response.error(NOT_EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if LocationValidator.is_latlng_valid(args["latlng"]):
                latlng = args["latlng"]
            else:
                latlng = None

            location = {
                "name": name,
                "latlng": latlng,
            }

            response = self.repository.location_repository.update_location(location_name, location)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, location_name):
            logger.debug(f"[DELETE] /locations/{location_name}")
            response = self.repository.location_repository.get_location(location_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.location_repository.delete_location(location_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
