from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models import ObservableProperty
from models.ObservableProperty import ObservableValueTypeEnum
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ObservablePropertyValidator

observable_property_parser = reqparse.RequestParser()
observable_property_parser.add_argument("name", type=str)
observable_property_parser.add_argument("value_type_to_measure", type=str)
observable_property_parser.add_argument("feature_of_interest_name", type=str)


class ObservablePropertyHandler:
    class ObservableProperties(Resource):
        def get(self):
            logger.debug(f"[GET] /observable-properties/")
            response = self.repository.observable_property_repository. \
                get_all_observable_properties()

            return Response.success(
                [translator.observable_property_translator(observable_property) for
                 observable_property in response])

        def post(self):
            logger.debug(f"[POST] /observable-properties/")
            args = observable_property_parser.parse_args()

            # Get ObservableProperty arguments
            if ObservablePropertyValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.observable_property_repository. \
                    get_observable_property(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ObservablePropertyValidator. \
                    is_value_type_to_measure_valid(args["value_type_to_measure"]):
                value_type_to_measure = args["value_type_to_measure"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ObservablePropertyValidator \
                    .is_feature_of_interest_name_valid(args["feature_of_interest_name"]):
                feature_of_interest_name = args["feature_of_interest_name"]

                response = self.repository.feature_of_interest_repository. \
                    get_feature_of_interest(feature_of_interest_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            observable_property = ObservableProperty(
                name=name,
                value_type_to_measure=ObservableValueTypeEnum(value_type_to_measure),
                feature_of_interest_name=feature_of_interest_name)

            result = self.repository.observable_property_repository.add_observable_property(
                observable_property)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class ObservableProperty(Resource):
        def get(self, observable_property_name):
            logger.debug(f"[GET] /observable-properties/{observable_property_name}")
            response = self.repository.observable_property_repository. \
                get_observable_property(observable_property_name)

            if response:
                return Response.success(translator.observable_property_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, observable_property_name):
            logger.debug(f"[PUT] /observable-properties/{observable_property_name}")
            args = observable_property_parser.parse_args()

            response = self.repository.observable_property_repository. \
                get_observable_property(observable_property_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get ObservableProperty arguments
            if ObservablePropertyValidator.is_name_valid(args["name"]):
                name = args["name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ObservablePropertyValidator. \
                    is_value_type_to_measure_valid(args["value_type_to_measure"]):
                value_type_to_measure = args["value_type_to_measure"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ObservablePropertyValidator \
                    .is_feature_of_interest_name_valid(args["feature_of_interest_name"]):
                feature_of_interest_name = args["feature_of_interest_name"]

                response = self.repository.feature_of_interest_repository. \
                    get_feature_of_interest(feature_of_interest_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            observable_property = {
                "name": name,
                "value_type_to_measure": ObservableValueTypeEnum(value_type_to_measure),
                "feature_of_interest_name": feature_of_interest_name
            }

            response = self.repository.observable_property_repository. \
                update_observable_property(observable_property_name, observable_property)

            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, observable_property_name):
            logger.debug(f"[DELETE] /observable-properties/{observable_property_name}")
            response = self.repository.observable_property_repository.get_observable_property(
                observable_property_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.observable_property_repository.delete_observable_property(
                observable_property_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
