# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class ThingType(Base):
    __tablename__ = "thing_type"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    things = relationship('Thing')

    def __str__(self):
        return f"{self.id}, {self.name}, {self.things}"
