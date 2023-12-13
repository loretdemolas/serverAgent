#serverAgent/base/routes.py

from flask import render_template
from . import base_blueprint

@base_blueprint.route('/')
def index():
    return render_template('base/base.html')
