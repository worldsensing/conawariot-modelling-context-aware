from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, NOT_EXISTS_THING, \
    NOT_THING_TYPE
from models import ObservationBoolean, ObservationString, ObservationInteger, ObservationFloat
from models.ObservableProperty import ObservableValueTypeEnum
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ObservationValidator

observation_parser = reqparse.RequestParser()
observation_parser.add_argument("sensor_name", type=str)
observation_parser.add_argument("time_start", type=str)
observation_parser.add_argument("time_end", type=str, required=False)
observation_parser.add_argument("value", type=str)


class ObservationHandler:
    class Observations(Resource):
        def get(self):
            logger.debug(f"[GET] /observations/")
            response = self.repository.observation_repository.get_all_observations()

            return Response.success(
                [translator.observation_translator(observation)
                 for observation in response])

        def post(self):
            logger.debug(f"[POST] /observations/")
            args = observation_parser.parse_args()

            # Get Observation arguments
            if ObservationValidator.is_sensor_name_valid(args["sensor_name"]):
                sensor_name = args["sensor_name"]

                sensor = self.repository.sensor_repository.get_sensor(sensor_name)
                if not sensor:
                    return Response.error(NOT_EXISTS_THING)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ObservationValidator.is_time_start_valid(args["time_start"]):
                time_start = args["time_start"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ObservationValidator.is_time_end_valid(args["time_end"]):
                time_end = args["time_end"]
            else:
                time_end = None

            if ObservationValidator.is_value_valid(args["value"]):
                value = args["value"]
            else:
                return Response.error(FIELD_NOT_VALID)

            sensor_observable_property_name = sensor.observable_property_name
            if sensor_observable_property_name is None:
                return Response.error(NOT_THING_TYPE)

            observable_property = self.repository.observable_property_repository. \
                get_observable_property(sensor_observable_property_name)

            if observable_property is None:
                return Response.error(NOT_THING_TYPE)

            observable_property_value_type = observable_property.value_type_to_measure
            if observable_property_value_type is None:
                return Response.error(NOT_THING_TYPE)

            observation = None
            if observable_property_value_type == ObservableValueTypeEnum.value_boolean:
                observation = ObservationBoolean(sensor_name=sensor_name,
                                                 time_start=time_start,
                                                 time_end=time_end,
                                                 value=(value == "True"))
            elif observable_property_value_type == ObservableValueTypeEnum.value_string:
                observation = ObservationString(sensor_name=sensor_name,
                                                time_start=time_start,
                                                time_end=time_end,
                                                value=value)
            elif observable_property_value_type == ObservableValueTypeEnum.value_integer:
                observation = ObservationInteger(sensor_name=sensor_name,
                                                 time_start=time_start,
                                                 time_end=time_end,
                                                 value=int(value))
            elif observable_property_value_type == ObservableValueTypeEnum.value_float:
                observation = ObservationFloat(sensor_name=sensor_name,
                                               time_start=time_start,
                                               time_end=time_end,
                                               value=float(value))

            if observation is None:
                return Response.error(GENERIC)

            result = self.repository.observation_repository.add_observation(observation)
            if result:
                return Response.success({"id": result})

            return Response.error(GENERIC)

    class Observation(Resource):
        def get(self, observation_id):
            logger.debug(f"[GET] /observations/{observation_id}")
            response = self.repository.observation_repository.get_observation(observation_id)

            if response:
                return Response.success(translator.observation_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def delete(self, observation_id):
            logger.debug(f"[DELETE] /observations/{observation_id}")
            response = self.repository.observation_repository.get_observation(observation_id)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.observation_repository.delete_observation(observation_id)
            if result:
                return Response.success({"id": result})

            return Response.error(GENERIC)
