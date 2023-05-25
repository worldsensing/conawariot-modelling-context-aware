from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship

from app.schemas.actuatable_property import ActuatableProperty
from app.schemas.observable_property import ObservableProperty


class FeatureOfInterest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)

    # Relations
    location_name: Optional[str] = Field(foreign_key="location.name")
    observable_properties: List[ObservableProperty] = Relationship()
    actuatable_properties: List[ActuatableProperty] = Relationship()
    #
