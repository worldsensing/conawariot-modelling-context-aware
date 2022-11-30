from database import actuator


class ActuatorRepository:
    @staticmethod
    def add_actuator(actuator_obj):
        return actuator.add_actuator(actuator_obj)

    @staticmethod
    def get_all_actuators():
        return actuator.get_all_actuators()

    @staticmethod
    def get_actuator(actuator_name):
        return actuator.get_actuator(actuator_name)

    @staticmethod
    def update_actuator(actuator_name, actuator_obj):
        return actuator.update_actuator(actuator_name, actuator_obj)

    @staticmethod
    def delete_actuator(actuator_name):
        return actuator.delete_actuator(actuator_name)
