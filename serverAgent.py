#serverAgent.py
from flask import Flask
import docker
import os
from compose import compose_blueprint
from home import home_blueprint
from terminal import terminal_blueprint
from base import base_blueprint
from terminal.routes import socketio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SOCKETIO_ASYNC_MODE'] = 'threading'  # Use 'threading' as the async mode

socketio.init_app(app, async_mode=app.config['SOCKETIO_ASYNC_MODE'])  # Initialize SocketIO with the app

app.register_blueprint(compose_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(terminal_blueprint)
app.register_blueprint(base_blueprint)
client = docker.from_env()

# Your other app configurations...

if __name__ == '__main__':
    # Check if the compose_files directory exists, and create it if not
    home_directory = os.path.expanduser("~")
    compose_directory = os.path.join(home_directory, "compose_files")

    if not os.path.exists(compose_directory):
        os.makedirs(compose_directory)

    socketio.run(app, debug=True)
