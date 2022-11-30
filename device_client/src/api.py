from flask import request, Blueprint

from src.core import post_sensor_observation

api = Blueprint("api", __name__)


@api.route("/observation", methods=["POST"])
def post():
    req_json = request.json

    value = req_json["value"]

    post_sensor_observation(value)

    return "OK"
