#serverAgent/compose/__init.py

from flask import Blueprint

compose_blueprint = Blueprint('compose', __name__, template_folder='templates')

from . import routes
