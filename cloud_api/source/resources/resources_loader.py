# -*- coding: utf-8 -*-
from flask_cors import CORS

from resources.api_handlers import ThingTypeHandler, ThingHandler, \
    ObservationHandler, ConditionRuleHandler, ContextAwareRulesHandler, LocationHandler, \
    ActuatablePropertyHandler, ActuationHandler, ActuatorHandler, EventRuleHandler, \
    EventRuleTypeHandler, FeatureOfInterestHandler, ObservablePropertyHandler, \
    ResponseProcedureHandler, PlatformHandler, SensorHandler


class Resources:
    @staticmethod
    def init_cors(app):
        cors_resources = [r"/actuatable-properties/*", r"/actuations/*", r"/actuators/*",
                          r"/context-aware-rules/*", r"/features-of-interest/*",
                          r"/locations/*", r"/observable-properties/*", r"/observations/*",
                          r"/platforms/*", r"/sensors/*", r"/things/*", r"/thing-types/*", ]

        cors_origins = ["http://localhost:3000", "http://localhost:8000",
                        "https://editor.swagger.io"]

        CORS(app, resources=cors_resources, origins=cors_origins)

    @staticmethod
    def load_resources(api):
        api.add_resource(ActuatablePropertyHandler.ActuatableProperties, "/actuatable-properties/",
                         strict_slashes=False)

        api.add_resource(ActuatablePropertyHandler.ActuatableProperty,
                         "/actuatable-properties/<string:actuatable_property_name>",
                         strict_slashes=False)

        api.add_resource(ActuationHandler.Actuations, "/actuations/",
                         strict_slashes=False)

        api.add_resource(ActuationHandler.Actuation, "/actuations/<string:actuation_id>",
                         strict_slashes=False)

        api.add_resource(ActuatorHandler.Actuators, "/actuators/",
                         strict_slashes=False)

        api.add_resource(ActuatorHandler.Actuator, "/actuators/<string:actuator_name>",
                         strict_slashes=False)

        api.add_resource(ConditionRuleHandler.ConditionRules, "/condition-rules/",
                         strict_slashes=False)

        api.add_resource(ConditionRuleHandler.ConditionRule,
                         "/condition-rules/<string:condition_rule_name>",
                         strict_slashes=False)

        api.add_resource(ContextAwareRulesHandler.ContextAwareRules,
                         "/context-aware-rules/",
                         strict_slashes=False)

        api.add_resource(ContextAwareRulesHandler.ContextAwareRule,
                         "/context-aware-rules/<string:context_aware_rule_name>",
                         strict_slashes=False)

        api.add_resource(ContextAwareRulesHandler.ContextAwareRulesComponents,
                         "/context-aware-rules/<string:context_aware_rule_name>/components",
                         strict_slashes=False)

        api.add_resource(EventRuleHandler.EventRules, "/event-rules/",
                         strict_slashes=False)

        api.add_resource(EventRuleHandler.EventRule,
                         "/event-rules/<string:event_rule_name>",
                         strict_slashes=False)

        api.add_resource(EventRuleTypeHandler.EventRuleTypes, "/event-rule-types/",
                         strict_slashes=False)

        api.add_resource(EventRuleTypeHandler.EventRuleType,
                         "/event-rule-types/<string:event_rule_type_name>",
                         strict_slashes=False)

        api.add_resource(FeatureOfInterestHandler.FeaturesOfInterest, "/features-of-interest/",
                         strict_slashes=False)

        api.add_resource(FeatureOfInterestHandler.FeatureOfInterest,
                         "/features-of-interest/<string:feature_of_interest_name>",
                         strict_slashes=False)

        api.add_resource(LocationHandler.Locations, "/locations/",
                         strict_slashes=False)

        api.add_resource(LocationHandler.Location, "/locations/<string:location_name>",
                         strict_slashes=False)

        api.add_resource(ObservablePropertyHandler.ObservableProperties, "/observable-properties/",
                         strict_slashes=False)

        api.add_resource(ObservablePropertyHandler.ObservableProperty,
                         "/observable-properties/<string:observable_property_name>",
                         strict_slashes=False)

        api.add_resource(ObservationHandler.Observations, "/observations/",
                         strict_slashes=False)

        api.add_resource(ObservationHandler.Observation, "/observations/<string:observation_id>",
                         strict_slashes=False)

        api.add_resource(PlatformHandler.Platforms, "/platforms/",
                         strict_slashes=False)

        api.add_resource(PlatformHandler.Platform, "/platforms/<string:platform_name>",
                         strict_slashes=False)

        api.add_resource(ResponseProcedureHandler.ResponseProcedures, "/response-procedures/",
                         strict_slashes=False)

        api.add_resource(ResponseProcedureHandler.ResponseProcedure,
                         "/response-procedures/<string:response_procedure_name>",
                         strict_slashes=False)

        api.add_resource(SensorHandler.Sensors, "/sensors/",
                         strict_slashes=False)

        api.add_resource(SensorHandler.Sensor, "/sensors/<string:sensor_name>",
                         strict_slashes=False)

        api.add_resource(SensorHandler.SensorObservation,
                         "/sensors/<string:sensor_name>/observations/",
                         strict_slashes=False)

        api.add_resource(ThingHandler.Things, "/things/",
                         strict_slashes=False)

        api.add_resource(ThingHandler.Thing, "/things/<string:thing_name>",
                         strict_slashes=False)

        api.add_resource(ThingTypeHandler.ThingTypes, "/thing-types/",
                         strict_slashes=False)

        api.add_resource(ThingTypeHandler.ThingType, "/thing-types/<string:thing_type_name>",
                         strict_slashes=False)
