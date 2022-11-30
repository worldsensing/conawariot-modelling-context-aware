import logging

from flask import Flask
from flask.logging import default_handler
from flask_restful import Api
from flask_socketio import SocketIO

from utils import db_uri

logger = logging.getLogger(__name__)

SQLALCHEMY_SETTINGS = {
    "SQLALCHEMY_DATABASE_URI": db_uri,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}

socketio = SocketIO()


def create_app(settings=SQLALCHEMY_SETTINGS):
    from resources.resources_loader import Resources

    app = Flask(__name__)
    api = Api(app)

    app.logger.removeHandler(default_handler)  # To remove flask default output
    app.logger.handlers.extend(logging.getLogger('gunicorn.error').handlers)
    app.logger.setLevel(logging.DEBUG)

    logger.info("Enabling CORS and setting wildcards")
    Resources.init_cors(app)

    logger.info("Connecting to the DB")
    app.config["SQLALCHEMY_DATABASE_URI"] = settings["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings["SQLALCHEMY_TRACK_MODIFICATIONS"]
    app.config['SECRET_KEY'] = 'DUMMYsecret!'  # TODO Change and add this to an ENV file

    socketio.init_app(app)

    with app.app_context():
        import database
        database.init_db()
        # TODO Future improvement
        # yield app

    Resources.load_resources(api)

    return app, database
