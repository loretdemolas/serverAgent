# home/__init__.py
from flask import Blueprint
from flask_socketio import SocketIO

home_blueprint = Blueprint('home', __name__, template_folder='templates')
socketio = SocketIO()  # Initialize SocketIO here

from . import routes  # Import routes after initializing socketio
