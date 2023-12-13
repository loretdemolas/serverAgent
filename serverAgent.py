#serverAgent.py
from flask import Flask
import docker
import os
from compose import compose_blueprint
from home import home_blueprint
from home.routes import additional_content_blueprint
from terminal import terminal_blueprint
from base import base_blueprint
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['SOCKETIO_ASYNC_MODE'] = 'threading'  # Use 'threading' as the async mode


app.register_blueprint(compose_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(additional_content_blueprint)
app.register_blueprint(terminal_blueprint)
app.register_blueprint(base_blueprint)
client = docker.from_env()

if __name__ == '__main__':
    # Check if the compose_files directory exists, and create it if not
    script_directory = os.path.dirname(os.path.abspath(__file__))
    compose_directory = os.path.join(script_directory, "compose_files")

    if not os.path.exists(compose_directory):
        os.makedirs(compose_directory)

    socketio.init_app(app, async_mode=app.config['SOCKETIO_ASYNC_MODE'])  # Initialize SocketIO with the app
    socketio.run(app, debug=True)