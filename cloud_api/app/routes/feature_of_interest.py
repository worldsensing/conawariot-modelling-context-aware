from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.database import get_session
from app.repository import feature_of_interest as feature_of_interest_repo, \
    location as location_repo
from app.schemas.feature_of_interest import FeatureOfInterest

router = APIRouter(prefix="/features-of-interest")


@router.get("/", response_model=List[FeatureOfInterest])
def get_features_of_interest(offset: int = 0, limit: int = Query(default=100, lte=100),
                             session: Session = Depends(get_session)):
    features_of_interest = feature_of_interest_repo.get_features_of_interest(offset=offset,
                                                                             limit=limit,
                                                                             session=session)
    return features_of_interest


@router.post("/", response_model=FeatureOfInterest)
def post_feature_of_interest(feature_of_interest: FeatureOfInterest,
                             session: Session = Depends(get_session)):
    db_feature_of_interest = feature_of_interest_repo.get_feature_of_interest(
        feature_of_interest_name=feature_of_interest.name, session=session)
    if db_feature_of_interest:
        raise HTTPException(status_code=400, detail="FeatureOfInterest name already registered")

    if feature_of_interest.location_name:
        db_location = location_repo.get_location(location_name=feature_of_interest.location_name,
                                                 session=session)
        if not db_location:
            raise HTTPException(status_code=404, detail="Location does not exist")

    return feature_of_interest_repo.create_feature_of_interest(
        feature_of_interest=feature_of_interest, session=session)


@router.get("/{feature_of_interest_name}/", response_model=FeatureOfInterest)
def get_feature_of_interest(feature_of_interest_name: str,
                            session: Session = Depends(get_session)):
    db_feature_of_interest = feature_of_interest_repo.get_feature_of_interest(
        feature_of_interest_name=feature_of_interest_name, session=session)
    if db_feature_of_interest is None:
        raise HTTPException(status_code=404, detail="FeatureOfInterest not found")

    return db_feature_of_interest


@router.delete("/{feature_of_interest_name}/", response_model=FeatureOfInterest)
def delete_feature_of_interest(feature_of_interest_name: str,
                               session: Session = Depends(get_session)):
    db_feature_of_interest = feature_of_interest_repo.get_feature_of_interest(
        feature_of_interest_name=feature_of_interest_name, session=session)
    if not db_feature_of_interest:
        raise HTTPException(status_code=400, detail="FeatureOfInterest name does not exist.")

    db_feature_of_interest = feature_of_interest_repo.delete_feature_of_interest(
        feature_of_interest_name=feature_of_interest_name, session=session)
    return db_feature_of_interest
