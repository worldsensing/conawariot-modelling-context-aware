# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base


class ContextAwareRule(Base):
    __tablename__ = "context_aware_rule"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    executing = Column(Boolean, default=True)

    event_rules = relationship('EventRule')
    condition_rules = relationship('ConditionRule')
    response_procedure = relationship('ResponseProcedure') # TODO Rename to response_procedures

    actuations = relationship('Actuation')

    def __str__(self):
        return f"{self.id}, {self.name}, {self.executing}, " \
               f"{self.event_rules}, {self.condition_rules}, {self.response_procedure}, " \
               f"{self.actuations}"
