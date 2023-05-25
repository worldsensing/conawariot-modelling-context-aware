from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import location as location_repo, thing as thing_repo, gateway as gateway_repo, \
    group as group_repo
from app.schemas.thing import Thing

router = APIRouter(prefix="/things")


@router.get("/", response_model=List[Thing])
def get_things(offset: int = 0, limit: int = Query(default=100, lte=100),
               session: Session = Depends(get_session)):
    things = thing_repo.get_things(offset=offset, limit=limit, session=session)
    return things


@router.post("/", response_model=Thing)
def post_thing(thing: Thing,
               session: Session = Depends(get_session)):
    db_thing = thing_repo.get_thing(thing_name=thing.name, session=session)
    if db_thing:
        raise HTTPException(status_code=400, detail="Thing name already registered")

    if thing.group_name:
        db_group = group_repo.get_group(group_name=thing.group_name,
                                        session=session)
        if not db_group:
            raise HTTPException(status_code=404, detail="Group does not exist")

    if thing.gateway_name:
        db_gateway = gateway_repo.get_gateway(gateway_name=thing.gateway_name,
                                              session=session)
        if not db_gateway:
            raise HTTPException(status_code=404, detail="Gateway does not exist")

    if thing.location_name:
        db_location = location_repo.get_location(location_name=thing.location_name,
                                                 session=session)
        if not db_location:
            raise HTTPException(status_code=400, detail="Location name does not exist")

    return thing_repo.create_thing(thing=thing, session=session)


@router.get("/{thing_name}/", response_model=Thing)
def get_thing(thing_name: str,
              session: Session = Depends(get_session)):
    db_thing = thing_repo.get_thing(thing_name=thing_name, session=session)
    if db_thing is None:
        raise HTTPException(status_code=404, detail="Thing not found")

    return db_thing


@router.delete("/{thing_name}/", response_model=Thing)
def delete_thing(thing_name: str,
                 session: Session = Depends(get_session)):
    db_thing = thing_repo.get_thing(thing_name=thing_name, session=session)
    if not db_thing:
        raise HTTPException(status_code=400, detail="Thing name does not exist.")

    db_thing = thing_repo.delete_thing(thing_name=thing_name, session=session)
    return db_thing
