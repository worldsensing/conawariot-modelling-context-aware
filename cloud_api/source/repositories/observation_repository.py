from database import observation


class ObservationRepository:
    @staticmethod
    def add_observation(observation_obj):
        return observation.add_observation(observation_obj)

    @staticmethod
    def get_all_observations():
        return observation.get_all_observations()

    @staticmethod
    def get_observation(observation_name):
        return observation.get_observation(observation_name)

    @staticmethod
    def delete_observation(observation_name):
        return observation.delete_observation(observation_name)

    @staticmethod
    def get_observations_filter_sensor(sensor_name):
        return observation.get_observations_filter_sensor(sensor_name)
