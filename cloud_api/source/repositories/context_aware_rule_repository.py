from database import context_aware_rule


class ContextAwareRuleRepository:
    @staticmethod
    def add_context_aware_rule(context_aware_rule_obj):
        return context_aware_rule.add_context_aware_rule(context_aware_rule_obj)

    @staticmethod
    def get_all_context_aware_rules():
        return context_aware_rule.get_all_context_aware_rules()

    @staticmethod
    def get_context_aware_rule(context_aware_rule_name):
        return context_aware_rule.get_context_aware_rule(context_aware_rule_name)

    @staticmethod
    def update_context_aware_rule(context_aware_rule_name, context_aware_rule_obj):
        return context_aware_rule.update_context_aware_rule(context_aware_rule_name,
                                                            context_aware_rule_obj)

    @staticmethod
    def delete_context_aware_rule(context_aware_rule_name):
        return context_aware_rule.delete_context_aware_rule(context_aware_rule_name)
