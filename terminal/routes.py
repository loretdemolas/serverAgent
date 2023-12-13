# serverAgent/terminal/routes.py
from flask import render_template
from . import terminal_blueprint
from flask_socketio import SocketIO, emit
import subprocess

socketio = SocketIO()  # Create SocketIO instance

@terminal_blueprint.route('/terminal')
def index():
    return render_template('terminal/terminal.html')

@socketio.on('input_command')
def handle_input_command(command):
    # Run the command in the terminal
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr

    # Emit the output to the client
    emit('output_result', {'output': output})
