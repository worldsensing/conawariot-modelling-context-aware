import enum
from typing import Optional, List

from sqlmodel import Column, Enum, Field, SQLModel, Relationship

from app.schemas.observation import Observation
from app.schemas.sensor import Sensor


class TypeOfObservations(enum.Enum):
    INTEGER_PROP = "integer"
    FLOAT_PROP = "float"
    BOOLEAN_PROP = "boolean"
    STRING_PROP = "string"
    DICT_PROP = "dict"


class ObservableProperty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    type_of_observation: TypeOfObservations = Field(
        sa_column=Column(Enum(TypeOfObservations), nullable=False))

    # Relations
    feature_of_interest_name: str = Field(nullable=False, foreign_key="featureofinterest.name")
    sensors: List["Sensor"] = Relationship(back_populates="observable_property")
    observations: List["Observation"] = Relationship()
    #
