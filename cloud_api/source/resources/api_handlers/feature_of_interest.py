from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models import FeatureOfInterest
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import FeatureOfInterestValidator

feature_of_interest_parser = reqparse.RequestParser()
feature_of_interest_parser.add_argument("name", type=str)
feature_of_interest_parser.add_argument("location_name", type=str)


class FeatureOfInterestHandler:
    class FeaturesOfInterest(Resource):
        def get(self):
            logger.debug(f"[GET] /features-of-interest/")
            response = self.repository.feature_of_interest_repository.get_all_features_of_interest()

            return Response.success(
                [translator.feature_of_interest_translator(feature_of_interest) for
                 feature_of_interest in response])

        def post(self):
            logger.debug(f"[POST] /features-of-interest/")
            args = feature_of_interest_parser.parse_args()

            # Get FeatureOfInterest arguments
            if FeatureOfInterestValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.feature_of_interest_repository. \
                    get_feature_of_interest(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if FeatureOfInterestValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(
                    location_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            feature_of_interest = FeatureOfInterest(
                name=name,
                location_name=location_name)

            result = self.repository.feature_of_interest_repository. \
                add_feature_of_interest(feature_of_interest)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class FeatureOfInterest(Resource):
        def get(self, feature_of_interest_name):
            logger.debug(f"[GET] /features-of-interest/{feature_of_interest_name}")
            response = self.repository.feature_of_interest_repository.get_feature_of_interest(
                feature_of_interest_name)

            if response:
                return Response.success(translator.feature_of_interest_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, feature_of_interest_name):
            logger.debug(f"[PUT] /features-of-interest/{feature_of_interest_name}")
            args = feature_of_interest_parser.parse_args()

            response = self.repository.feature_of_interest_repository.get_feature_of_interest(
                feature_of_interest_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get FeatureOfInterest arguments
            if FeatureOfInterestValidator.is_name_valid(args["name"]):
                name = args["name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if FeatureOfInterestValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(location_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            feature_of_interest = {
                "name": name,
                "location_name": location_name
            }

            response = self.repository.feature_of_interest_repository.update_feature_of_interest(
                feature_of_interest_name, feature_of_interest)

            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, feature_of_interest_name):
            logger.debug(f"[DELETE] /features-of-interest/{feature_of_interest_name}")
            response = self.repository.feature_of_interest_repository.get_feature_of_interest(
                feature_of_interest_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.feature_of_interest_repository.delete_feature_of_interest(
                feature_of_interest_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
