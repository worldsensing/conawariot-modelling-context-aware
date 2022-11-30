import json

import pytest

from fixtures import ThingTypeDictFactory, ThingDictFactory, \
    ThingTypeFactory2DB, LocationDictFactory, LocationFactory2DB, PlatformDictFactory, \
    SensorDictFactory, ObservablePropertyDictFactory, FeatureOfInterestDictFactory, \
    ObservationIntegerDictFactory, ActuationDictFactory, ContextAwareRuleDictFactory
from test_api_actuation import assert_actuations
from test_api_context_aware_rule import assert_context_aware_rules
from test_api_feature_of_interest import assert_features_of_interest
from test_api_location import assert_locations
from test_api_observable_property import assert_observable_properties
from test_api_observation import assert_observations
from test_api_platform import assert_platforms
from test_api_sensor import assert_sensors
from test_api_thing import assert_things
from test_api_thing_type import assert_thing_types


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB()


@pytest.fixture
def create_location():
    return LocationFactory2DB(name="MyLocation1")


@pytest.mark.parametrize(
    "test_input_thing_type, test_input_location, test_input_platform, test_input_thing, "
    "test_input_feature_of_interest, test_input_observable_property, test_input_sensor, "
    "test_input_observation, test_input_context_aware_rule, test_input_actuation", [
        (["ThingType1"],
         ["Location1", "41.2, 2.1"],
         ["Platform1", "Location1"],
         ["Thing1", "ThingType1", "Location1"],
         ["FeatureOfInterest1", "Location1"],
         ["ObservableProperty1", "BOOLEAN", "FeatureOfInterest1"],
         ["Sensor1", "Thing1", "ObservableProperty1", "Location1"],
         ["Sensor1", "False", "2020-03-18T12:00:00+00:00"],
         ["Rule1", True],
         ["IGNORED", "Rule1", "2020-03-18T12:00:00+00:00", "2020-03-18T12:00:10+00:00"],
         )
    ])
def test_full_api(api_client, orm_client,
                  test_input_thing_type, test_input_location, test_input_platform, test_input_thing,
                  test_input_feature_of_interest, test_input_observable_property, test_input_sensor,
                  test_input_observation, test_input_context_aware_rule, test_input_actuation):
    # ThingType
    ## Create ThingType element
    thing_type = ThingTypeDictFactory(name=test_input_thing_type[0])
    rv = api_client.post("/thing-types/", json=thing_type)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == thing_type["name"]

    ## Check ThingType creation
    rv = api_client.get(f"/thing-types/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_thing_types(response_content, thing_type)

    # Location
    ## Create Location element
    location = LocationDictFactory(name=test_input_location[0],
                                   latlng=test_input_location[1])
    rv = api_client.post("/locations/", json=location)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == location["name"]

    ## Check Location creation
    rv = api_client.get(f"/locations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_locations(response_content, location)

    # Platform checks
    ## Create Platform element
    platform = PlatformDictFactory(name=test_input_platform[0],
                                   location_name=test_input_platform[1])
    rv = api_client.post("/platforms/", json=platform)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == platform["name"]

    ## Check Platform creation
    rv = api_client.get(f"/platforms/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_platforms(response_content, platform)

    # Thing checks
    ## Create Thing element
    thing = ThingDictFactory(name=test_input_thing[0],
                             type_name=test_input_thing[1],
                             location_name=test_input_thing[2])

    rv = api_client.post("/things/", json=thing)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == thing["name"]

    ## Check Thing creation
    rv = api_client.get(f"/things/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_things(response_content, thing)

    # FeatureOfInterest checks
    ## Create FeatureOfInterest element
    feature_of_interest = FeatureOfInterestDictFactory(
        name=test_input_feature_of_interest[0],
        location_name=test_input_feature_of_interest[1])

    rv = api_client.post("/features-of-interest/", json=feature_of_interest)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == feature_of_interest["name"]

    ## Check FeatureOfInterest creation
    rv = api_client.get(f"/features-of-interest/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_features_of_interest(response_content, feature_of_interest)

    # ObservableProperty checks
    ## Create ObservableProperty element
    observable_property = ObservablePropertyDictFactory(
        name=test_input_observable_property[0],
        value_type_to_measure=test_input_observable_property[1],
        feature_of_interest_name=test_input_observable_property[2])

    rv = api_client.post("/observable-properties/", json=observable_property)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == observable_property["name"]

    ## Check ObservableProperty creation
    rv = api_client.get(f"/observable-properties/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_observable_properties(response_content, observable_property)

    # Sensor checks
    ## Create Sensor element
    sensor = SensorDictFactory(name=test_input_sensor[0],
                               thing_name=test_input_sensor[1],
                               observable_property_name=test_input_sensor[2],
                               location_name=test_input_sensor[3])

    rv = api_client.post("/sensors/", json=sensor)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == sensor["name"]

    ## Check Sensor creation
    rv = api_client.get(f"/sensors/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_sensors(response_content, sensor)

    # Observation checks
    ## Create Observation element
    observation = ObservationIntegerDictFactory(sensor_name=test_input_observation[0],
                                                value=test_input_observation[1],
                                                time_start=test_input_observation[2])

    rv = api_client.post("/observations/", json=observation)
    assert rv.status_code == 200, rv.data
    observation_id = json.loads(rv.data)["data"]["id"]

    ## Check Observation creation
    rv = api_client.get(f"/observations/{observation_id}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_observations(response_content, observation)

    # ContextAwareRule checks
    ## Create ContextAwareRule element
    context_aware_rule = ContextAwareRuleDictFactory(
        name=test_input_context_aware_rule[0],
        executing=test_input_context_aware_rule[1],
    )

    rv = api_client.post("/context-aware-rules/", json=context_aware_rule)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["name"]
    assert response_content == context_aware_rule["name"]

    ## Check ContextAwareRule creation
    rv = api_client.get(f"/context-aware-rules/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_context_aware_rules(response_content, context_aware_rule)

    # Actuation checks
    ## Create Actuation element
    actuation = ActuationDictFactory(observation_id=observation_id,
                                     context_aware_rule_name=test_input_actuation[1],
                                     time_start=test_input_actuation[2],
                                     time_end=test_input_actuation[3])

    rv = api_client.post("/actuations/", json=actuation)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)["data"]["id"]

    ## Check Actuation creation
    rv = api_client.get(f"/actuations/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)["data"]
    assert_actuations(response_content, actuation)

    # TODO ActuatableProperty

    # TODO Actuator
