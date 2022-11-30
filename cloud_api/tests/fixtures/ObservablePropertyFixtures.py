from functools import partial

import factory

from models import ObservableProperty
from models.ObservableProperty import ObservableValueTypeEnum
from .fixtures import dict_factory


class AbstractObservablePropertyFactory(factory.Factory):
    class Meta:
        model = ObservableProperty
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Light1"
    feature_of_interest_name = "Room33"
    value_type_to_measure = ObservableValueTypeEnum.value_boolean


class ObservablePropertyFactory(AbstractObservablePropertyFactory):
    pass


ObservablePropertyFactory._meta.exclude = ("id",)
ObservablePropertyDictFactory = partial(dict_factory, ObservablePropertyFactory)


class ObservablePropertyFactory2DB(AbstractObservablePropertyFactory,
                                   factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
