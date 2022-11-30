from flask_socketio import emit

from app import socketio, logger


def __emit(event_name, event_data=None, broadcast=False):
    logger.info(f"Message emitted: {event_name} {event_data}")

    emit(event_name, event_data, broadcast=broadcast)


@socketio.on("/connect")
def test_connect():
    logger.info("Client connected")
    __emit("/on_connect_checks")


# This route cannot be changed as the socket-io-client implements "disconnect" as callback
@socketio.on("disconnect")
def test_disconnect():
    logger.info("Client disconnected")


@socketio.on("/forward_message_to_clients")
def forward_message_to_clients(args):
    logger.info(f"Message received: /forward_message_to_clients {args}")

    event_name = args["event_name"]
    event_data = args["data"]

    __emit(event_name, event_data, broadcast=True)
