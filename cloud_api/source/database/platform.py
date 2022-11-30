from database import session


def add_platform(platform):
    try:
        session.add(platform)
        session.flush()
        name = platform.name
        session.commit()
    except:
        session.rollback()
        return None

    return name


def get_all_platforms():
    from models.Platform import Platform

    try:
        platforms = session.query(Platform) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return platforms


def get_platform(platform_name):
    from models.Platform import Platform

    try:
        platform = session.query(Platform) \
            .filter_by(name=platform_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return platform


def update_platform(platform_name, platform):
    from models.Platform import Platform

    try:
        session.query(Platform) \
            .filter_by(name=platform_name) \
            .update(platform)
        session.commit()
    except:
        session.rollback()
        return None

    return platform_name


def delete_platform(platform_name):
    from models.Platform import Platform

    try:
        session.query(Platform) \
            .filter_by(name=platform_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return platform_name


def get_platforms_filter_platform_type(platform_type):
    from models.Platform import Platform

    try:
        platforms = session.query(Platform) \
            .filter_by(type=platform_type) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return platforms
