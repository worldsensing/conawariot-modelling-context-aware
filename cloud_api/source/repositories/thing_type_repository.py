from database import thing_type


class ThingTypeRepository:
    @staticmethod
    def add_thing_type(thing_type_obj):
        return thing_type.add_thing_type(thing_type_obj)

    @staticmethod
    def get_all_thing_types():
        return thing_type.get_all_thing_types()

    @staticmethod
    def get_thing_type(thing_type_name):
        return thing_type.get_thing_type(thing_type_name)

    @staticmethod
    def update_thing_type(thing_type_name, thing_type_obj):
        return thing_type.update_thing_type(thing_type_name, thing_type_obj)

    @staticmethod
    def delete_thing_type(thing_type_name):
        return thing_type.delete_thing_type(thing_type_name)
