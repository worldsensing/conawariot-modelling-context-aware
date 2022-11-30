# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, String
from sqlalchemy.orm import relationship

from database import Base
from translators import model_translators


class Actuation(Base):
    __tablename__ = "actuation"
    id = Column(Integer, primary_key=True, nullable=False)
    observation_id = Column(Integer, ForeignKey("observation.id",
                                                ondelete="SET NULL"))  # TODO Should be a list
    context_aware_rule_name = Column(String(32),
                                     ForeignKey("context_aware_rule.name", ondelete="SET NULL"))
    time_start = Column(DateTime(timezone=True), nullable=True)
    time_end = Column(DateTime(timezone=True), nullable=True)

    actuators = relationship("ActuatorActuation", back_populates="actuation")

    UniqueConstraint("observation_id", "context_aware_rule_name", "time_start")

    def __str__(self):
        return f"{self.id}, {self.observation_id}, {self.context_aware_rule_name}, " \
               f"{model_translators.translate_datetime(self.time_start)}, " \
               f"{model_translators.translate_datetime(self.time_end)}, {self.actuators}"
