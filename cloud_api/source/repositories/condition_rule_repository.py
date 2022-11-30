from database import condition_rule


class ConditionRuleRepository:
    @staticmethod
    def add_condition_rule(condition_rule_obj):
        return condition_rule.add_condition_rule(condition_rule_obj)

    @staticmethod
    def get_all_condition_rules():
        return condition_rule.get_all_condition_rules()

    @staticmethod
    def get_condition_rule(condition_rule_name):
        return condition_rule.get_condition_rule(condition_rule_name)

    @staticmethod
    def update_condition_rule(condition_rule_name, condition_rule_obj):
        return condition_rule.update_condition_rule(condition_rule_name, condition_rule_obj)

    @staticmethod
    def delete_condition_rule(condition_rule_name):
        return condition_rule.delete_condition_rule(condition_rule_name)
