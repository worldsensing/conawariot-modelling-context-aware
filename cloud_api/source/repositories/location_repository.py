from database import location


class LocationRepository:
    @staticmethod
    def add_location(location_obj):
        return location.add_location(location_obj)

    @staticmethod
    def get_all_locations():
        return location.get_all_locations()

    @staticmethod
    def get_location(location_name):
        return location.get_location(location_name)

    @staticmethod
    def update_location(location_name, location_obj):
        return location.update_location(location_name, location_obj)

    @staticmethod
    def delete_location(location_name):
        return location.delete_location(location_name)
