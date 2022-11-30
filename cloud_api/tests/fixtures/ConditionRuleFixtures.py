from functools import partial

import factory

from models import ConditionRule
from .fixtures import dict_factory


class AbstractConditionRuleFactory(factory.Factory):
    class Meta:
        model = ConditionRule
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Rule1"
    context_aware_rule_name = "BR1"
    event_rule_1_name = "EV_RULE_1"
    event_rule_2_name = "EV_RULE_2"
    condition_rule_1_name = None
    condition_rule_2_name = None


class ConditionRuleFactory(AbstractConditionRuleFactory):
    pass


ConditionRuleFactory._meta.exclude = ("id",)
ConditionRuleDictFactory = partial(dict_factory, ConditionRuleFactory)


class ConditionRuleFactory2DB(AbstractConditionRuleFactory,
                              factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
