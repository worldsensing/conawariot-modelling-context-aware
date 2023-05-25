from sqlmodel import Session, select

from app.schemas.feature_of_interest import FeatureOfInterest


def get_feature_of_interest(feature_of_interest_name: str, session: Session):
    return session.exec(
        select(FeatureOfInterest)
        .where(FeatureOfInterest.name == feature_of_interest_name)
    ).first()


def get_features_of_interest(offset: int, limit: int, session: Session):
    return session.exec(
        select(FeatureOfInterest)
        .offset(offset).limit(limit)) \
        .all()


def create_feature_of_interest(feature_of_interest: FeatureOfInterest, session: Session):
    db_feature_of_interest = FeatureOfInterest(
        name=feature_of_interest.name,
        location_name=feature_of_interest.location_name
    )
    session.add(db_feature_of_interest)
    session.commit()
    session.refresh(db_feature_of_interest)
    return db_feature_of_interest


def delete_feature_of_interest(feature_of_interest_name: str, session: Session):
    feature_of_interest = get_feature_of_interest(feature_of_interest_name, session)
    session.delete(feature_of_interest)
    session.commit()
    return feature_of_interest
