import datetime
from functools import partial

import factory
from dateutil.tz import UTC
from factory.fuzzy import FuzzyDateTime

from models import Observation, ObservationBoolean, ObservationString, ObservationInteger, \
    ObservationFloat
from .fixtures import dict_factory


class AbstractObservationFactory(factory.Factory):
    class Meta:
        model = Observation
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    sensor_name = "Sensor1"
    # time_start = "2020-03-18T12:00:00+00:00"
    time_start = FuzzyDateTime(datetime.datetime(2019, 1, 1, tzinfo=UTC),
                               datetime.datetime(2020, 1, 1, tzinfo=UTC),
                               force_microsecond=0)
    time_end = None


class ObservationFactory(AbstractObservationFactory):
    pass


ObservationFactory._meta.exclude = ("id",)
ObservationDictFactory = partial(dict_factory, ObservationFactory)


class ObservationFactory2DB(AbstractObservationFactory, factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"


class AbstractObservationBooleanFactory(AbstractObservationFactory):
    class Meta:
        model = ObservationBoolean
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    value = True


class ObservationBooleanFactory(AbstractObservationBooleanFactory):
    pass


ObservationBooleanFactory._meta.exclude = ("id",)
ObservationBooleanDictFactory = partial(dict_factory, ObservationBooleanFactory)


class ObservationBooleanFactory2DB(AbstractObservationBooleanFactory,
                                   factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"


class AbstractObservationStringFactory(AbstractObservationFactory):
    class Meta:
        model = ObservationString
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    value = "TEST"


class ObservationStringFactory(AbstractObservationStringFactory):
    pass


ObservationStringFactory._meta.exclude = ("id",)
ObservationStringDictFactory = partial(dict_factory, ObservationStringFactory)


class ObservationStringFactory2DB(AbstractObservationStringFactory,
                                  factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"


class AbstractObservationIntegerFactory(AbstractObservationFactory):
    class Meta:
        model = ObservationInteger
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    value = 1


class ObservationIntegerFactory(AbstractObservationIntegerFactory):
    pass


ObservationIntegerFactory._meta.exclude = ("id",)
ObservationIntegerDictFactory = partial(dict_factory, ObservationIntegerFactory)


class ObservationIntegerFactory2DB(AbstractObservationIntegerFactory,
                                   factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"


class AbstractObservationFloatFactory(AbstractObservationFactory):
    class Meta:
        model = ObservationFloat
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    value = 0.1


class ObservationFloatFactory(AbstractObservationFloatFactory):
    pass


ObservationFloatFactory._meta.exclude = ("id",)
ObservationFloatDictFactory = partial(dict_factory, ObservationFloatFactory)


class ObservationFloatFactory2DB(AbstractObservationFloatFactory,
                                 factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
