from database import session


def add_feature_of_interest(feature_of_interest):
    try:
        session.add(feature_of_interest)
        session.flush()
        name = feature_of_interest.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_feature_of_interests():
    from models.FeatureOfInterest import FeatureOfInterest

    try:
        feature_of_interests = session.query(FeatureOfInterest) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return feature_of_interests


def get_feature_of_interest(feature_of_interest_name):
    from models.FeatureOfInterest import FeatureOfInterest

    try:
        feature_of_interests = session.query(FeatureOfInterest) \
            .filter_by(name=feature_of_interest_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return feature_of_interests


def update_feature_of_interest(feature_of_interest_name, feature_of_interest):
    from models.FeatureOfInterest import FeatureOfInterest

    try:
        session.query(FeatureOfInterest) \
            .filter_by(name=feature_of_interest_name) \
            .update(feature_of_interest)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return feature_of_interest_name


def delete_feature_of_interest(feature_of_interest_name):
    from models.FeatureOfInterest import FeatureOfInterest

    try:
        session.query(FeatureOfInterest) \
            .filter_by(name=feature_of_interest_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return feature_of_interest_name
