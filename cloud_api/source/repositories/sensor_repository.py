from database import sensor


class SensorRepository:
    @staticmethod
    def add_sensor(sensor_obj):
        return sensor.add_sensor(sensor_obj)

    @staticmethod
    def get_all_sensors():
        return sensor.get_all_sensors()

    @staticmethod
    def get_sensor(sensor_name):
        return sensor.get_sensor(sensor_name)

    @staticmethod
    def update_sensor(sensor_name, sensor_obj):
        return sensor.update_sensor(sensor_name, sensor_obj)

    @staticmethod
    def delete_sensor(sensor_name):
        return sensor.delete_sensor(sensor_name)
