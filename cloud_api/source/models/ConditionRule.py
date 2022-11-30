# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from database import Base


class ConditionRuleComparationTypeEnum(enum.Enum):
    AND = "AND"
    OR = "OR"
    NAND = "NAND"
    NOR = "NOR"
    XOR = "XOR"


class ConditionRule(Base):
    __tablename__ = "condition_rule"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    context_aware_rule_name = Column(String(32), ForeignKey("context_aware_rule.name"),
                                     nullable=False)
    event_rule_1_name = Column(String(32), ForeignKey("event_rule.name", ondelete="SET NULL"))
    event_rule_2_name = Column(String(32), ForeignKey("event_rule.name", ondelete="SET NULL"))
    condition_rule_1_name = Column(String(32),
                                   ForeignKey("condition_rule.name", ondelete="SET NULL"))
    condition_rule_2_name = Column(String(32),
                                   ForeignKey("condition_rule.name", ondelete="SET NULL"))

    condition_comparation_type = Column(Enum(ConditionRuleComparationTypeEnum), nullable=False)

    def __str__(self):
        return f"{self.id}, {self.name}, {self.event_rule_1_name}, {self.event_rule_2_name}, " \
               f"{self.condition_rule_1_name}, {self.condition_rule_2_name}, " \
               f"{self.condition_comparation_type.value}"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "context_aware_rule_name": self.context_aware_rule_name,
            "event_rule_1_name": self.event_rule_1_name,
            "event_rule_2_name": self.event_rule_2_name,
            "condition_rule_1_name": self.condition_rule_1_name,
            "condition_rule_2_name": self.condition_rule_2_name,
            "condition_comparation_type": self.condition_comparation_type.value
        }
