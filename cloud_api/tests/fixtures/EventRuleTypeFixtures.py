from functools import partial

import factory

from models import EventRuleType
from .fixtures import dict_factory


class AbstractEventRuleTypeFactory(factory.Factory):
    class Meta:
        model = EventRuleType
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "SENSOR_SENSOR_EQUALS_INTEGER_1"
    event_rule_type = "SENSOR_SENSOR"
    event_rule_comparation_type = "EQUALS"
    event_rule_value_type = "INTEGER"


class EventRuleTypeFactory(AbstractEventRuleTypeFactory):
    pass


EventRuleTypeFactory._meta.exclude = ("id",)
EventRuleTypeDictFactory = partial(dict_factory, EventRuleTypeFactory)


class EventRuleTypeFactory2DB(AbstractEventRuleTypeFactory,
                              factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
