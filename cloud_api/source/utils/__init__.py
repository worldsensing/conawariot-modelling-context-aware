# -*- coding: utf-8 -*-
"""
Utils methods.
"""
import json
import logging
from datetime import datetime

from utils import environment

logger = logging.getLogger(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            # For consistency with the API, we add the timezone marker Z
            return o.isoformat() + "Z"
        else:
            return json.JSONEncoder.default(self, o)


class JSONDecoder:
    def decode(self, text):
        return json.loads(text)


def construct_db_uri(db_configuration):
    return "postgresql://%s:%s@%s:%s/%s" % (
        db_configuration["POSTGRES_USER"], db_configuration["POSTGRES_PASSWORD"],
        db_configuration["POSTGRES_HOST"], db_configuration["POSTGRES_PORT"],
        db_configuration["POSTGRES_DATABASE"])


db_uri = construct_db_uri(environment.env_database())
