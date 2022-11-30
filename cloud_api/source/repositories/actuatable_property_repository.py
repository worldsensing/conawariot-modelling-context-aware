from database import actuatable_property


class ActuatablePropertyRepository:
    @staticmethod
    def add_actuatable_property(actuatable_property_obj):
        return actuatable_property.add_actuatable_property(actuatable_property_obj)

    @staticmethod
    def get_all_actuatable_properties():
        return actuatable_property.get_all_actuatable_properties()

    @staticmethod
    def get_actuatable_property(actuatable_property_name):
        return actuatable_property.get_actuatable_property(actuatable_property_name)

    @staticmethod
    def update_actuatable_property(actuatable_property_name, actuatable_property_obj):
        return actuatable_property.update_actuatable_property(actuatable_property_name,
                                                              actuatable_property_obj)

    @staticmethod
    def delete_actuatable_property(actuatable_property_name):
        return actuatable_property.delete_actuatable_property(actuatable_property_name)
