import datetime


# Will return datetime in this format '2022-11-07T15:45:27.875580+00:00'
def get_current_datetime():
    return datetime.datetime.now()


def get_current_datetime_str():
    return f"{datetime.datetime.now()}"