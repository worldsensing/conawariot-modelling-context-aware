from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID, \
    NOT_EXISTS_LOCATION
from models import Platform
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import PlatformValidator

platform_parser = reqparse.RequestParser()
platform_parser.add_argument("name", type=str)
platform_parser.add_argument("location_name", type=str, required=False)


class PlatformHandler:
    class Platforms(Resource):
        def get(self):
            logger.debug(f"[GET] /platforms/")
            response = self.repository.platform_repository.get_all_platforms()

            return Response.success(
                [translator.platform_translator(platform) for platform in response])

        def post(self):
            logger.debug(f"[POST] /platforms/")
            args = platform_parser.parse_args()

            # Get Platform arguments
            if PlatformValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.platform_repository.get_platform(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if PlatformValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(location_name)
                if response is None:
                    return Response.error(NOT_EXISTS_LOCATION)
            else:
                location_name = None

            platform = Platform(name=name, location_name=location_name)

            result = self.repository.platform_repository.add_platform(platform)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class Platform(Resource):
        def get(self, platform_name):
            logger.debug(f"[GET] /platforms/{platform_name}")
            response = self.repository.platform_repository.get_platform(platform_name)

            if response:
                return Response.success(translator.platform_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, platform_name):
            logger.debug(f"[PUT] /platforms/{platform_name}")
            args = platform_parser.parse_args()

            response = self.repository.platform_repository.get_platform(platform_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get Platform arguments
            if PlatformValidator.is_name_valid(args["name"]):
                name = args["name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if PlatformValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            platform = {
                "name": name,
                "location_name": location_name
            }

            response = self.repository.platform_repository.update_platform(platform_name, platform)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, platform_name):
            logger.debug(f"[DELETE] /platforms/{platform_name}")
            response = self.repository.platform_repository.get_platform(platform_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.platform_repository.delete_platform(platform_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)

    class PlatformObservation(Resource):
        def get(self, platform_name):
            logger.debug(f"[GET] UNUSED")
            response = self.repository.platform_repository.get_platform(platform_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            response = self.repository.platform_repository.get_observations_filter_platform(
                platform_name)

            return Response.success(
                [translator.observation_translator(observation) for observation in response])
