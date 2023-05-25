from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import gateway as gateway_repo, group as group_repo, thing as thing_repo
from app.repository import location as location_repo
from app.schemas.gateway import Gateway

router = APIRouter(prefix="/gateways")


@router.get("/", response_model=List[Gateway])
def get_gateways(offset: int = 0, limit: int = Query(default=100, lte=100),
                 session: Session = Depends(get_session)):
    gateways = gateway_repo.get_gateways(offset=offset, limit=limit, session=session)
    return gateways


@router.post("/", response_model=Gateway)
def post_gateway(gateway: Gateway,
                 session: Session = Depends(get_session)):
    db_gateway = gateway_repo.get_gateway(gateway_name=gateway.name, session=session)
    if db_gateway:
        raise HTTPException(status_code=400, detail="Gateway name already registered")

    if gateway.group_name:
        db_group = group_repo.get_group(group_name=gateway.group_name,
                                        session=session)
        if not db_group:
            raise HTTPException(status_code=404, detail="Group does not exist")

    if gateway.thing_name:
        db_thing = thing_repo.get_thing(thing_name=gateway.thing_name,
                                        session=session)
        if not db_thing:
            raise HTTPException(status_code=404, detail="Thing does not exist")

    if gateway.location_name:
        db_location = location_repo.get_location(location_name=gateway.location_name,
                                                 session=session)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location does not exist")

    return gateway_repo.create_gateway(gateway=gateway, session=session)


@router.get("/{gateway_name}/", response_model=Gateway)
def get_gateway(gateway_name: str,
                session: Session = Depends(get_session)):
    db_gateway = gateway_repo.get_gateway(gateway_name=gateway_name, session=session)
    if db_gateway is None:
        raise HTTPException(status_code=404, detail="Gateway not found")

    return db_gateway


@router.delete("/{gateway_name}/", response_model=Gateway)
def delete_gateway(gateway_name: str,
                   session: Session = Depends(get_session)):
    db_gateway = gateway_repo.get_gateway(gateway_name=gateway_name, session=session)
    if not db_gateway:
        raise HTTPException(status_code=400, detail="Gateway name does not exist.")

    db_gateway = gateway_repo.delete_gateway(gateway_name=gateway_name, session=session)
    return db_gateway
