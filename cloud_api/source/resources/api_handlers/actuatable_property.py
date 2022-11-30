from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models import ActuatableProperty
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ActuatablePropertyValidator

actuatable_property_parser = reqparse.RequestParser()
actuatable_property_parser.add_argument("name", type=str)
actuatable_property_parser.add_argument("feature_of_interest_name", type=str)


class ActuatablePropertyHandler:
    class ActuatableProperties(Resource):
        def get(self):
            logger.debug(f"[GET] /actuatable-properties/")
            response = self.repository.actuatable_property_repository. \
                get_all_actuatable_properties()

            return Response.success(
                [translator.actuatable_property_translator(actuatable_property) for
                 actuatable_property in response])

        def post(self):
            logger.debug(f"[POST] /actuatable-properties/")
            args = actuatable_property_parser.parse_args()

            # Get ActuatableProperty arguments
            if ActuatablePropertyValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.actuatable_property_repository. \
                    get_actuatable_property(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuatablePropertyValidator \
                    .is_feature_of_interest_name_valid(args["feature_of_interest_name"]):
                feature_of_interest_name = args["feature_of_interest_name"]

                response = self.repository.feature_of_interest_repository. \
                    get_feature_of_interest(feature_of_interest_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            actuatable_property = ActuatableProperty(
                name=name,
                feature_of_interest_name=feature_of_interest_name)

            result = self.repository.actuatable_property_repository.add_actuatable_property(
                actuatable_property)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class ActuatableProperty(Resource):
        def get(self, actuatable_property_name):
            logger.debug(f"[GET] /actuatable-properties/{actuatable_property_name}")
            response = self.repository.actuatable_property_repository.get_actuatable_property(
                actuatable_property_name)

            if response:
                return Response.success(translator.actuatable_property_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, actuatable_property_name):
            logger.debug(f"[PUT] /actuatable-properties/{actuatable_property_name}")
            args = actuatable_property_parser.parse_args()

            response = self.repository.actuatable_property_repository.get_actuatable_property(
                actuatable_property_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get ActuatableProperty arguments
            if ActuatablePropertyValidator.is_name_valid(args["name"]):
                name = args["name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ActuatablePropertyValidator \
                    .is_feature_of_interest_name_valid(args["feature_of_interest_name"]):
                feature_of_interest_name = args["feature_of_interest_name"]

                response = self.repository.feature_of_interest_repository. \
                    get_feature_of_interest(feature_of_interest_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            actuatable_property = {
                "name": name,
                "feature_of_interest_name": feature_of_interest_name
            }

            response = self.repository.actuatable_property_repository \
                .update_actuatable_property(actuatable_property_name, actuatable_property)

            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, actuatable_property_name):
            logger.debug(f"[DELETE] /actuatable-properties/{actuatable_property_name}")
            response = self.repository.actuatable_property_repository. \
                get_actuatable_property(actuatable_property_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.actuatable_property_repository. \
                delete_actuatable_property(actuatable_property_name)

            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
