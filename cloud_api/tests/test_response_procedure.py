import pytest

from fixtures import ContextAwareRuleFactory2DB, ResponseProcedureFactory2DB, ActuatorFactory2DB, \
    ThingFactory2DB, ThingTypeFactory2DB, ActuatablePropertyFactory2DB, \
    FeatureOfInterestFactory2DB, LocationFactory2DB


@pytest.fixture
def create_feature_of_interest():
    return FeatureOfInterestFactory2DB(name="Person")


@pytest.fixture
def create_actuatable_property(create_feature_of_interest):
    return ActuatablePropertyFactory2DB(name="Leg", feature_of_interest_name="Person")


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="RainModule")


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation2")


@pytest.fixture
def create_thing(create_thing_type, create_location):
    return ThingFactory2DB(name="RainModuleA", type_name="RainModule", location_name="MyLocation2")


@pytest.fixture
def create_actuator(create_thing, create_actuatable_property, create_location):
    return ActuatorFactory2DB(name="ACTUATOR1", thing_name="RainModuleA",
                              actuatable_property_name="Leg", location_name="MyLocation2")


@pytest.fixture
def create_context_aware_rule():
    return ContextAwareRuleFactory2DB(name="BR1")


@pytest.mark.parametrize("test_input, test_output", [
    (["RP1", "BR1", "PT1", "ACTUATOR1"],
     ["0, RP1, BR1, PT1, ACTUATOR1"])
])
def test_response_procedure_to_string(api_client, orm_client, create_context_aware_rule,
                                      create_actuator,
                                      test_input, test_output):
    response_procedure = ResponseProcedureFactory2DB(
        name=test_input[0],
        context_aware_rule_name=test_input[1],
        procedure_type_name=test_input[2],
        actuator_name=test_input[3])

    assert response_procedure.__str__() == test_output[0]
