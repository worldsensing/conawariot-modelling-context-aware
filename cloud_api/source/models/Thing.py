# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Thing(Base):
    __tablename__ = "thing"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    type_name = Column(String(32), ForeignKey('thing_type.name', ondelete="SET NULL"))
    location_name = Column(String(32), ForeignKey('location.name', ondelete="SET NULL"))
    sensors = relationship('Sensor')
    actuators = relationship('Actuator')

    platforms = relationship("ThingStatus", back_populates="thing")

    def __str__(self):
        return f"{self.id}, {self.name}, {self.type_name}, {self.location_name}, {self.sensors}" \
               f", {self.actuators}, {self.platforms}"
