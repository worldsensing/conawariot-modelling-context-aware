from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID, \
    NOT_EXISTS_LOCATION
from models import Sensor
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import SensorValidator

sensor_parser = reqparse.RequestParser()
sensor_parser.add_argument("name", type=str)
sensor_parser.add_argument("thing_name", type=str)
sensor_parser.add_argument("observable_property_name", type=str)
sensor_parser.add_argument("location_name", type=str, required=False)


class SensorHandler:
    class Sensors(Resource):
        def get(self):
            logger.debug(f"[GET] /sensors/")
            response = self.repository.sensor_repository.get_all_sensors()

            return Response.success(
                [translator.sensor_translator(sensor) for sensor in response])

        def post(self):
            logger.debug(f"[POST] /sensors/")
            args = sensor_parser.parse_args()

            # Get Sensor arguments
            if SensorValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.sensor_repository.get_sensor(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if SensorValidator.is_thing_name_valid(args["thing_name"]):
                thing_name = args["thing_name"]

                response = self.repository.thing_repository.get_thing(thing_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if SensorValidator.is_observable_property_name_valid(args["observable_property_name"]):
                observable_property_name = args["observable_property_name"]

                response = self.repository.observable_property_repository. \
                    get_observable_property(observable_property_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if SensorValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(location_name)
                if response is None:
                    return Response.error(NOT_EXISTS_LOCATION)
            else:
                location_name = None

            sensor = Sensor(name=name, thing_name=thing_name,
                            observable_property_name=observable_property_name,
                            location_name=location_name)

            result = self.repository.sensor_repository.add_sensor(sensor)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class Sensor(Resource):
        def get(self, sensor_name):
            logger.debug(f"[GET] /sensors/{sensor_name}")
            response = self.repository.sensor_repository.get_sensor(sensor_name)

            if response:
                return Response.success(translator.sensor_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, sensor_name):
            logger.debug(f"[PUT] /sensors/{sensor_name}")
            args = sensor_parser.parse_args()

            response = self.repository.sensor_repository.get_sensor(sensor_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get Sensor arguments
            if SensorValidator.is_name_valid(args["name"]):
                name = args["name"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if SensorValidator.is_thing_name_valid(args["thing_name"]):
                thing_name = args["thing_name"]

                response = self.repository.thing_repository.get_thing(thing_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if SensorValidator.is_thing_name_valid(args["observable_property_name"]):
                observable_property_name = args["observable_property_name"]

                response = self.repository.observable_property_repository.get_observable_property(
                    observable_property_name)
                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if SensorValidator.is_location_name_valid(args["location_name"]):
                location_name = args["location_name"]

                response = self.repository.location_repository.get_location(location_name)
                if response is None:
                    return Response.error(NOT_EXISTS_LOCATION)
            else:
                location_name = None

            sensor = {
                "name": name,
                "thing_name": thing_name,
                "observable_property_name": observable_property_name,
                "location_name": location_name
            }

            response = self.repository.sensor_repository.update_sensor(sensor_name, sensor)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, sensor_name):
            logger.debug(f"[DELETE] /sensors/{sensor_name}")
            response = self.repository.sensor_repository.get_sensor(sensor_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.sensor_repository.delete_sensor(sensor_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)

    class SensorObservation(Resource):
        def get(self, sensor_name):
            logger.debug(f"[GET] /sensors/{sensor_name}/observations/")
            response = self.repository.sensor_repository.get_sensor(sensor_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            response = self.repository.observation_repository. \
                get_observations_filter_sensor(sensor_name)

            return Response.success(
                [translator.observation_translator(observation) for observation in response])
