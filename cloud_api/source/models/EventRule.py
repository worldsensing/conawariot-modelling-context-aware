# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float

from database import Base


class EventRule(Base):
    __tablename__ = "event_rule"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    context_aware_rule_name = Column(String(32), ForeignKey("context_aware_rule.name"),
                                     nullable=False)
    event_rule_type_name = Column(String(32),
                                  ForeignKey('event_rule_type.name', ondelete="SET NULL"),
                                  nullable=False)
    sensor_1_name = Column(String(32), ForeignKey("sensor.name", ondelete="SET NULL"),
                           nullable=False)
    sensor_2_name = Column(String(32), ForeignKey("sensor.name", ondelete="SET NULL"))

    value_to_compare_boolean = Column(Boolean)
    value_to_compare_string = Column(String(32))
    value_to_compare_integer = Column(Integer)
    value_to_compare_float = Column(Float)

    def __str__(self):
        return f"{self.id}, {self.name}, {self.context_aware_rule_name}, " \
               f"{self.event_rule_type_name}, {self.sensor_1_name}, {self.sensor_2_name}, " \
               f"{self.value_to_compare_boolean}, {self.value_to_compare_string}," \
               f"{self.value_to_compare_integer}, {self.value_to_compare_float}"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "context_aware_rule_name": self.context_aware_rule_name,
            "event_rule_type_name": self.event_rule_type_name,
            "sensor_1_name": self.sensor_1_name,
            "sensor_2_name": self.sensor_2_name,
            "value_to_compare_boolean": self.value_to_compare_boolean,
            "value_to_compare_string": self.value_to_compare_string,
            "value_to_compare_integer": self.value_to_compare_integer,
            "value_to_compare_float": self.value_to_compare_float,
        }
