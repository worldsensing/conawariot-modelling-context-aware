# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ActuatorActuation(Base):
    __tablename__ = 'actuator_actuation'
    actuator_name = Column(ForeignKey('actuator.name'), primary_key=True)
    actuation_id = Column(ForeignKey('actuation.id'), primary_key=True)

    actuator = relationship("Actuator", back_populates="actuations")
    actuation = relationship("Actuation", back_populates="actuators")

    def __str__(self):
        return f"{self.actuator_name}, {self.actuation_id}"
