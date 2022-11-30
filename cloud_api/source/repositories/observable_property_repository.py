from database import observable_property


class ObservablePropertyRepository:
    @staticmethod
    def add_observable_property(observable_property_obj):
        return observable_property.add_observable_property(observable_property_obj)

    @staticmethod
    def get_all_observable_properties():
        return observable_property.get_all_observable_properties()

    @staticmethod
    def get_observable_property(observable_property_name):
        return observable_property.get_observable_property(observable_property_name)

    @staticmethod
    def update_observable_property(observable_property_name, observable_property_obj):
        return observable_property.update_observable_property(observable_property_name,
                                                              observable_property_obj)

    @staticmethod
    def delete_observable_property(observable_property_name):
        return observable_property.delete_observable_property(observable_property_name)
