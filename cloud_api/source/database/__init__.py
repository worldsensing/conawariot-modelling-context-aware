# -*- coding: utf-8 -*-
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from utils import db_uri

logger = logging.getLogger(__name__)

engine = create_engine(db_uri, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=True,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()
metadata = Base.metadata


def init_db():
    Base.metadata.create_all(engine, checkfirst=True)


def close():
    session.close()
    engine.dispose()
