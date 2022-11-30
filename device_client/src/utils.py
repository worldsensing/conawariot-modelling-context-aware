from datetime import datetime


def get_current_time():
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
