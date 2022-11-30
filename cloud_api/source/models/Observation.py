# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, \
    Boolean, Float

from database import Base
from translators import model_translators


class Observation(Base):
    __tablename__ = "observation"
    id = Column(Integer, primary_key=True, nullable=False)
    sensor_name = Column(String(32), ForeignKey("sensor.name", ondelete="SET NULL"))
    time_start = Column(DateTime(timezone=True), nullable=False)
    time_end = Column(DateTime(timezone=True), nullable=True)
    type = Column(String(16))

    UniqueConstraint("sensor_name", "time_start")

    __mapper_args__ = {
        "polymorphic_identity": "observation",
        "polymorphic_on": type
    }


class ObservationBoolean(Observation):
    __tablename__ = "obs_boolean"
    id = Column(Integer, ForeignKey("observation.id", ondelete="cascade"), primary_key=True)
    value = Column(Boolean, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "obs_boolean",
    }

    def __str__(self):
        return f"{self.id}, {self.sensor_name}, {self.value}" \
               f", {model_translators.translate_datetime(self.time_start)}" \
               f", {model_translators.translate_datetime(self.time_end)}"


class ObservationString(Observation):
    __tablename__ = "obs_string"
    id = Column(Integer, ForeignKey("observation.id", ondelete="cascade"), primary_key=True)
    value = Column(String(64), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "obs_string",
    }

    def __str__(self):
        return f"{self.id}, {self.sensor_name}, {self.value}" \
               f", {model_translators.translate_datetime(self.time_start)}" \
               f", {model_translators.translate_datetime(self.time_end)}"


class ObservationInteger(Observation):
    __tablename__ = "obs_integer"
    id = Column(Integer, ForeignKey("observation.id", ondelete="cascade"), primary_key=True)
    value = Column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "obs_integer",
    }

    def __str__(self):
        return f"{self.id}, {self.sensor_name}, {self.value}" \
               f", {model_translators.translate_datetime(self.time_start)}" \
               f", {model_translators.translate_datetime(self.time_end)}"


class ObservationFloat(Observation):
    __tablename__ = "obs_float"
    id = Column(Integer, ForeignKey("observation.id", ondelete="cascade"), primary_key=True)
    value = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "obs_float",
    }

    def __str__(self):
        return f"{self.id}, {self.sensor_name}, {self.value}" \
               f", {model_translators.translate_datetime(self.time_start)}" \
               f", {model_translators.translate_datetime(self.time_end)}"
