from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship

from app.schemas.actuation import Actuation
from app.schemas.actuator import Actuator


class ActuatableProperty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    # Relations
    feature_of_interest_name: str = Field(nullable=False, foreign_key="featureofinterest.name")
    actuators: List["Actuator"] = Relationship(back_populates="actuatable_property")
    actuations: List["Actuation"] = Relationship()
    #
