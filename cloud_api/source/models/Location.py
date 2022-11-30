# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from database import Base


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    latlng = Column(String(32), nullable=True)

    def __str__(self):
        return f"{self.id}, {self.name}, {self.latlng}"
