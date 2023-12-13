#serverAgent/terminal/__init.py
from flask import Blueprint

terminal_blueprint = Blueprint('terminal', __name__, template_folder='templates')

from . import routes
