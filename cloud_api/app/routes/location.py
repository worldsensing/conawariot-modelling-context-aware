from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import location as location_repo
from app.schemas.location import Location

router = APIRouter(prefix="/locations")


@router.get("/", response_model=List[Location])
def get_locations(offset: int = 0, limit: int = Query(default=100, lte=100),
                  session: Session = Depends(get_session)):
    locations = location_repo.get_locations(offset=offset, limit=limit, session=session)
    return locations


@router.post("/", response_model=Location)
def post_location(location: Location,
                  session: Session = Depends(get_session)):
    db_location = location_repo.get_location(location_name=location.name, session=session)
    if db_location:
        raise HTTPException(status_code=400, detail="Location name already registered")
    return location_repo.create_location(location=location, session=session)


@router.get("/{location_name}/", response_model=Location)
def get_location(location_name: str,
                 session: Session = Depends(get_session)):
    db_location = location_repo.get_location(location_name=location_name, session=session)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    return db_location


@router.delete("/{location_name}/", response_model=Location)
def delete_location(location_name: str,
                    session: Session = Depends(get_session)):
    get_location(location_name=location_name, session=session)

    db_location = location_repo.delete_location(location_name=location_name, session=session)
    return db_location
