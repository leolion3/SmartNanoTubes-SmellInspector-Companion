import json
from typing import Tuple

from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

from middleware.connections_handler import MiddlewareConnectionHandler
from ml_helper import ml_helper

ml_helper.init()
app = Flask(__name__, static_folder='build/static', template_folder='build')
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, origins=['*'])
middleware: MiddlewareConnectionHandler = MiddlewareConnectionHandler()


def get_error_message(*args) -> Tuple[str, int]:
    """
    Builds a 401 response with the missing parameters.
    :param args: arguments required in the request body.
    :return: a json error message and a 401 status code.
    """
    if not len(args):
        return json.dumps({'error': 'Error in request.'}), 401
    if len(args) == 1:
        return json.dumps({'error': f'Missing data. Required: "{args[0]}"'}), 401
    args = ' and '.join([f'"{arg}"' for arg in args])
    return json.dumps({'error': f'Missing data. Required: {args}'}), 401


def validate_body(body, args) -> bool:
    """
    Validates the request json body.
    :param body: request body.
    :param args: arguments required in the request body.
    :return: True if the request is valid, false otherwise.
    """
    if not body:
        return False
    for arg in args:
        if arg not in body:
            return False
    return True


@app.route('/static/<path:path>')
def serve_static(path):
    """
    Serves static content from React build directory.
    """
    return send_from_directory('build/static', path)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """
    Serves React app from build directory.
    All React-Router routes are served from the index file using JS.
    """
    return send_from_directory('build', 'index.html')


@app.route('/get_serial_ports', methods=['GET'])
def get_serial_ports():
    return middleware.get_serial_ports()


@app.route('/get_devices', methods=['GET'])
def get_devices():
    return middleware.get_all_devices()


@app.route('/get_connected_devices', methods=['GET'])
def get_connected_devices():
    return middleware.get_connected_devices()


@app.route('/get_disconnected_devices', methods=['GET'])
def get_disconnected_devices():
    return middleware.get_disconnected_devices()


@app.route('/get_free_devices', methods=['GET'])
def get_free_devices():
    return middleware.get_free_devices()


@app.route('/get_active_tests', methods=['GET'])
def get_active_tests():
    return middleware.get_active_tests()


@app.route('/get_substances', methods=['GET'])
def get_substances():
    return middleware.get_substances()


@app.route('/add_substance', methods=['POST'])
def add_substance():
    body = request.get_json()
    args = ['substance_name', 'substance_quantity']
    if not validate_body(body, args):
        return get_error_message(*args)
    return middleware.add_substance(body[args[0]], body[args[1]])


@app.route('/update_substance', methods=['POST'])
def update_substance():
    body = request.get_json()
    args = ['substance_id', 'substance_name', 'substance_quantity']
    if not validate_body(body, args):
        return get_error_message(*args)
    return middleware.update_substance(body[args[0]], body[args[1]], body[args[2]])


@app.route('/delete_substance', methods=['POST'])
def delete_substance():
    body = request.get_json()
    args = ['substance_id']
    if not validate_body(body, args):
        return get_error_message(*args)
    return middleware.delete_substance(body[args[0]])


@app.route('/get_test_substance', methods=['POST'])
def get_substance():
    body = request.get_json()
    args = ["test_name"]
    if not validate_body(body, args):
        return get_error_message(*args)
    return middleware.get_test_substance(body[args[0]])


@app.route('/update_test_substance', methods=['POST'])
def update_test_substance():
    body = request.get_json()
    args = ['test_name', 'substance_id']
    if not validate_body(body, args):
        return get_error_message(*args)
    return middleware.update_test_substance(body[args[0]], body[args[1]])


@app.route('/start_stop_test', methods=['POST'])
def start_test():
    body = request.get_json()
    args = ["test_name", "device_nickname"]
    if not validate_body(body, args):
        return get_error_message(*args)
    data_acquisition_enabled = body.get('data_acquisition_enabled', True)
    return middleware.start_stop_test(body[args[0]], body[args[1]], data_acquisition_enabled, socketio)


@app.route('/register_device', methods=['POST'])
def register_device():
    body = request.get_json()
    args = ["device_nickname", "com_port"]
    if not validate_body(body, args):
        return get_error_message(*args)
    return middleware.register_device(body[args[0]], body[args[1]])


@app.route('/de_register_device', methods=['POST'])
def de_register_device():
    body = request.get_json()
    args = ["device_nickname"]
    if not validate_body(body, args):
        return get_error_message(*args)
    return middleware.de_register_device(body['device_nickname'])


@app.route('/get_ml_data', methods=['GET'])
def get_ml_data():
    ml_helper.init()
    return {
        'status': 'success'
    }, 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
