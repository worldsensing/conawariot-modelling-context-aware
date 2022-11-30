from database import event_rule_type


class EventRuleTypeRepository:
    @staticmethod
    def add_event_rule_type(event_rule_type_obj):
        return event_rule_type.add_event_rule_type(event_rule_type_obj)

    @staticmethod
    def get_all_event_rule_types():
        return event_rule_type.get_all_event_rule_types()

    @staticmethod
    def get_event_rule_type(event_rule_type_name):
        return event_rule_type.get_event_rule_type(event_rule_type_name)

    @staticmethod
    def update_event_rule_type(event_rule_type_name, event_rule_type_obj):
        return event_rule_type.update_event_rule_type(event_rule_type_name, event_rule_type_obj)

    @staticmethod
    def delete_event_rule_type(event_rule_type_name):
        return event_rule_type.delete_event_rule_type(event_rule_type_name)
