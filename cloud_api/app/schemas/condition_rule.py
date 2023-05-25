import enum
from typing import Optional

from sqlmodel import Column, Enum, Field, SQLModel


# TODO This class is not reflected in the Ontology conceptual overview
class ConditionRuleComparationTypeEnum(enum.Enum):
    AND = "AND"
    OR = "OR"
    NAND = "NAND"
    NOR = "NOR"
    XOR = "XOR"


class ConditionRule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    # Relations
    # TODO This should be a list, now we assume is One-to-Many, should be Many-to-Many
    context_aware_rule_name: str = Field(nullable=False, foreign_key="contextawarerule.name")
    condition_comparation_type: ConditionRuleComparationTypeEnum = Field(
        sa_column=Column(Enum(ConditionRuleComparationTypeEnum)))
    event_rule_1_name: Optional[str] = Field(foreign_key="eventrule.name")
    event_rule_2_name: Optional[str] = Field(foreign_key="eventrule.name")
    # These checks have to be done in runtime
    condition_rule_1_name: Optional[str]  # = Field(foreign_key="conditionrule.name")
    condition_rule_2_name: Optional[str]  # = Field(foreign_key="conditionrule.name")
    #
