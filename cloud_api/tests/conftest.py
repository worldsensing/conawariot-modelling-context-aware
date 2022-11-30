import logging

import pytest

import database
from app import create_app
from fixtures import ThingFactory2DB, ThingTypeFactory2DB, ObservationFactory2DB, \
    ObservationBooleanFactory2DB, ObservationStringFactory2DB, ObservationIntegerFactory2DB, \
    ObservationFloatFactory2DB, ContextAwareRuleFactory2DB, LocationFactory2DB, \
    SensorFactory2DB, FeatureOfInterestFactory2DB, ActuatablePropertyFactory2DB, \
    ActuationFactory2DB, ActuatorFactory2DB, ObservablePropertyFactory2DB, PlatformFactory2DB, \
    ActuatorActuationFactory2DB, ThingStatusFactory2DB, ConditionRuleFactory2DB, \
    EventRuleFactory2DB, ResponseProcedureFactory2DB, EventRuleTypeFactory2DB
from utils import db_uri

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module", autouse=True)
def api_client():
    SQLALCHEMY_SETTINGS = {
        "SQLALCHEMY_DATABASE_URI": db_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    }

    print("API_CLIENT START")
    app, db = create_app(settings=SQLALCHEMY_SETTINGS)
    ThingFactory2DB._meta.sqlalchemy_session = db.session
    ThingTypeFactory2DB._meta.sqlalchemy_session = db.session
    ObservationFactory2DB._meta.sqlalchemy_session = db.session
    ObservationBooleanFactory2DB._meta.sqlalchemy_session = db.session
    ObservationStringFactory2DB._meta.sqlalchemy_session = db.session
    ObservationIntegerFactory2DB._meta.sqlalchemy_session = db.session
    ObservationFloatFactory2DB._meta.sqlalchemy_session = db.session
    ContextAwareRuleFactory2DB._meta.sqlalchemy_session = db.session
    LocationFactory2DB._meta.sqlalchemy_session = db.session
    SensorFactory2DB._meta.sqlalchemy_session = db.session
    FeatureOfInterestFactory2DB._meta.sqlalchemy_session = db.session
    ActuatablePropertyFactory2DB._meta.sqlalchemy_session = db.session
    ActuationFactory2DB._meta.sqlalchemy_session = db.session
    ActuatorFactory2DB._meta.sqlalchemy_session = db.session
    ObservablePropertyFactory2DB._meta.sqlalchemy_session = db.session
    PlatformFactory2DB._meta.sqlalchemy_session = db.session
    ActuatorActuationFactory2DB._meta.sqlalchemy_session = db.session
    ThingStatusFactory2DB._meta.sqlalchemy_session = db.session
    ConditionRuleFactory2DB._meta.sqlalchemy_session = db.session
    EventRuleFactory2DB._meta.sqlalchemy_session = db.session
    EventRuleTypeFactory2DB._meta.sqlalchemy_session = db.session
    ResponseProcedureFactory2DB._meta.sqlalchemy_session = db.session
    yield app.test_client()
    print("API_CLIENT END")
    db.session.close()
    db.engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def clear_tables():
    print("CLEAR_TABLES START")
    yield
    session = database.session
    for name, table in database.metadata.tables.items():
        session.execute(f'ALTER TABLE "{table.name}" DISABLE TRIGGER ALL;')
        session.execute(table.delete())
        session.execute(f'ALTER TABLE "{table.name}" ENABLE TRIGGER ALL;')
    print("CLEAR_TABLES END")
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def orm_client(api_client):
    client = database
    client.init_db()
    print("ORM_CLIENT START")
    yield client
    ThingFactory2DB.reset_sequence(value=0, force=True)
    ThingTypeFactory2DB.reset_sequence(value=0, force=True)
    ObservationFactory2DB.reset_sequence(value=0, force=True)
    ObservationBooleanFactory2DB.reset_sequence(value=0, force=True)
    ObservationStringFactory2DB.reset_sequence(value=0, force=True)
    ObservationIntegerFactory2DB.reset_sequence(value=0, force=True)
    ObservationFloatFactory2DB.reset_sequence(value=0, force=True)
    ContextAwareRuleFactory2DB.reset_sequence(value=0, force=True)
    LocationFactory2DB.reset_sequence(value=0, force=True)
    SensorFactory2DB.reset_sequence(value=0, force=True)
    FeatureOfInterestFactory2DB.reset_sequence(value=0, force=True)
    ActuatablePropertyFactory2DB.reset_sequence(value=0, force=True)
    ActuationFactory2DB.reset_sequence(value=0, force=True)
    ActuatorFactory2DB.reset_sequence(value=0, force=True)
    ObservablePropertyFactory2DB.reset_sequence(value=0, force=True)
    PlatformFactory2DB.reset_sequence(value=0, force=True)
    ActuatorActuationFactory2DB.reset_sequence(value=0, force=True)
    ThingStatusFactory2DB.reset_sequence(value=0, force=True)
    ConditionRuleFactory2DB.reset_sequence(value=0, force=True)
    EventRuleFactory2DB.reset_sequence(value=0, force=True)
    EventRuleTypeFactory2DB.reset_sequence(value=0, force=True)
    ResponseProcedureFactory2DB.reset_sequence(value=0, force=True)
    print("ORM_CLIENT END")
    client.close()
