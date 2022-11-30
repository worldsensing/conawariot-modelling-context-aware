from functools import partial

import factory

from models import EventRule
from .fixtures import dict_factory


class AbstractEventRuleFactory(factory.Factory):
    class Meta:
        model = EventRule
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Rule1"
    context_aware_rule_name = "BR1"
    event_rule_type_name = "SENSOR_SENSOR_EQUALS_INTEGER_1"
    sensor_1_name = "SENSOR1"
    sensor_2_name = None

    value_to_compare_boolean = None
    value_to_compare_string = None
    value_to_compare_integer = None
    value_to_compare_float = None


class EventRuleFactory(AbstractEventRuleFactory):
    pass


EventRuleFactory._meta.exclude = ("id",)
EventRuleDictFactory = partial(dict_factory, EventRuleFactory)


class EventRuleFactory2DB(AbstractEventRuleFactory,
                          factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
