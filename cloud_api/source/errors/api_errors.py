"""
Custom errors factory.
"""


class ApiError(Exception):
    def __init__(self, message, http_code, internal_code, params=()):
        self.message = message.format(*params)
        self.http_code = http_code
        self.internal_code = internal_code
        super(Exception, self).__init__(self.message)


GENERIC = ApiError("An unexpected error has occurred.", 500, 0)
FIELD_NOT_VALID = ApiError("Field is not valid.", 422, 4)
INVALID_ID = ApiError("Invalid id/name format.", 404, 1)
EXISTS_ID = ApiError("Id/name does exist.", 400, 2)
NOT_EXISTS_ID = ApiError("Id does not exist.", 404, 3)
NOT_EXISTS_THING = ApiError("thing-name does not exist.", 404, 10)
NOT_EXISTS_LOCATION = ApiError("location name does not exists.", 404, 11)
NOT_THING_TYPE = ApiError("Thing does not have a valid ThingType.", 400, 15)
THING_TYPE_HAS_TYPE = ApiError("ThingType is being used by, at least, one thing.", 400, 17)
