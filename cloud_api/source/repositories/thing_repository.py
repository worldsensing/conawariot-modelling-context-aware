from database import thing


class ThingRepository:
    @staticmethod
    def add_thing(thing_obj):
        return thing.add_thing(thing_obj)

    @staticmethod
    def get_all_things():
        return thing.get_all_things()

    @staticmethod
    def get_thing(thing_name):
        return thing.get_thing(thing_name)

    @staticmethod
    def update_thing(thing_name, thing_obj):
        return thing.update_thing(thing_name, thing_obj)

    @staticmethod
    def delete_thing(thing_name):
        return thing.delete_thing(thing_name)

    @staticmethod
    def get_things_filter_thing_type(thing_type_obj):
        return thing.get_things_filter_thing_type(thing_type_obj)
