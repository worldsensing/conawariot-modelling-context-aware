from functools import partial

import factory

from models import FeatureOfInterest
from .fixtures import dict_factory


class AbstractFeatureOfInterestFactory(factory.Factory):
    class Meta:
        model = FeatureOfInterest
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Person"
    location_name = None


class FeatureOfInterestFactory(AbstractFeatureOfInterestFactory):
    pass


FeatureOfInterestFactory._meta.exclude = ("id",)
FeatureOfInterestDictFactory = partial(dict_factory, FeatureOfInterestFactory)


class FeatureOfInterestFactory2DB(AbstractFeatureOfInterestFactory,
                                  factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
