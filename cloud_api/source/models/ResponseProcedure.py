# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class ResponseProcedure(Base):
    __tablename__ = "response_procedure"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    context_aware_rule_name = Column(String(32), ForeignKey("context_aware_rule.name"),
                                     nullable=False)
    procedure_type_name = Column(String(32), nullable=False)  # TODO Add foreign key

    actuator_name = Column(String(32), ForeignKey("actuator.name"),
                           nullable=False)  # TODO Should be a list

    def __str__(self):
        return f"{self.id}, {self.name}, {self.context_aware_rule_name}, " \
               f"{self.procedure_type_name}, {self.actuator_name}"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "context_aware_rule_name": self.context_aware_rule_name,
            "procedure_type_name": self.procedure_type_name,
            "actuator_name": self.actuator_name
        }
