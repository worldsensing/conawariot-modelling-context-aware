from functools import partial

import factory

from models import ContextAwareRule
from .fixtures import dict_factory


class AbstractContextAwareRuleFactory(factory.Factory):
    class Meta:
        model = ContextAwareRule
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Rule1"
    executing = True


class ContextAwareRuleFactory(AbstractContextAwareRuleFactory):
    pass


ContextAwareRuleFactory._meta.exclude = ("id",)
ContextAwareRuleDictFactory = partial(dict_factory, ContextAwareRuleFactory)


class ContextAwareRuleFactory2DB(AbstractContextAwareRuleFactory,
                                 factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
