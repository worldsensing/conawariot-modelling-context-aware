import datetime
from functools import partial

import factory
from dateutil.tz import UTC
from factory.fuzzy import FuzzyDateTime

from models import Actuation
from .fixtures import dict_factory


class AbstractActuationFactory(factory.Factory):
    class Meta:
        model = Actuation
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    observation_id = 0
    context_aware_rule_name = "Rule1"
    # time_start = "2020-03-18T12:00:00+00:00"
    time_start = FuzzyDateTime(datetime.datetime(2019, 1, 1, tzinfo=UTC),
                               datetime.datetime(2020, 1, 1, tzinfo=UTC),
                               force_microsecond=0)
    time_end = None


class ActuationFactory(AbstractActuationFactory):
    pass


ActuationFactory._meta.exclude = ("id",)
ActuationDictFactory = partial(dict_factory, ActuationFactory)


class ActuationFactory2DB(AbstractActuationFactory,
                          factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
