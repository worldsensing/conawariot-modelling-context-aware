from database import event_rule


class EventRuleRepository:
    @staticmethod
    def add_event_rule(event_rule_obj):
        return event_rule.add_event_rule(event_rule_obj)

    @staticmethod
    def get_all_event_rules():
        return event_rule.get_all_event_rules()

    @staticmethod
    def get_event_rule(event_rule_name):
        return event_rule.get_event_rule(event_rule_name)

    @staticmethod
    def update_event_rule(event_rule_name, event_rule_obj):
        return event_rule.update_event_rule(event_rule_name, event_rule_obj)

    @staticmethod
    def delete_event_rule(event_rule_name):
        return event_rule.delete_event_rule(event_rule_name)
