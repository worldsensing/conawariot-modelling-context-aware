# -*- coding: utf-8 -*-
import datetime


def translate_datetime(m_datetime):
    if m_datetime is None:
        return None
    return m_datetime.replace(tzinfo=datetime.timezone.utc).isoformat()
