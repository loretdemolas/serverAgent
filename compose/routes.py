#serverAgent/compose/routes.py
from flask import Flask, render_template, request, redirect, url_for
import docker
import os

client = docker.from_env()

from . import compose_blueprint

@compose_blueprint.route('/compose')
def index():
    return render_template('compose/compose.html')

# Function to get a list of compose files in the home directory
def get_compose_files():
    home_directory = os.path.expanduser("~")
    compose_directory = os.path.join(home_directory, "compose_files")

    # Ensure the compose directory exists
    if not os.path.exists(compose_directory):
        os.makedirs(compose_directory)

    # Get a list of compose files in the directory
    compose_files = [f for f in os.listdir(compose_directory) if os.path.isfile(os.path.join(compose_directory, f))]
    return compose_files

@compose_blueprint.route('/compose')
def compose():
    compose_files = get_compose_files()
    return render_template('compose.html', compose_files=compose_files)

@compose_blueprint.route('/write-compose', methods=['POST'])
def write_compose_file():
    compose_content = request.form['compose_content']
    file_name = request.form['file_name']

    # Save the compose content to a file in the compose_files directory
    home_directory = os.path.expanduser("~")
    compose_directory = os.path.join(home_directory, "compose_files")

    with open(os.path.join(compose_directory, file_name), 'w') as file:
        file.write(compose_content)

    # Run docker-compose with the specified file
    # (Replace with your logic to run docker-compose)

    return redirect(url_for('compose.index'))

@compose_blueprint.route('/edit-compose/<file_name>')
def edit_compose_file(file_name):
    # Get the content of the compose file
    home_directory = os.path.expanduser("~")
    compose_directory = os.path.join(home_directory, "compose_files")

    with open(os.path.join(compose_directory, file_name), 'r') as file:
        compose_content = file.read()

    return render_template('edit_compose.html', file_name=file_name, compose_content=compose_content)

@compose_blueprint.route('/update-compose/<file_name>', methods=['POST'])
def update_compose_file(file_name):
    new_compose_content = request.form['compose_content']

    # Save the updated compose content to the file
    home_directory = os.path.expanduser("~")
    compose_directory = os.path.join(home_directory, "compose_files")

    with open(os.path.join(compose_directory, file_name), 'w') as file:
        file.write(new_compose_content)

    # Run docker-compose with the specified file
    # (Replace with your logic to run docker-compose)

    return redirect(url_for('compose.index'))

@compose_blueprint.route('/delete-compose/<file_name>')
def delete_compose_file(file_name):
    # Delete the compose file
    home_directory = os.path.expanduser("~")
    compose_directory = os.path.join(home_directory, "compose_files")
    file_path = os.path.join(compose_directory, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect(url_for('compose.index'))

@compose_blueprint.route('/run-compose/<file_name>')
def run_compose_file(file_name):
    # Run docker-compose with the specified file
    # (Replace with your logic to run docker-compose)

    return redirect(url_for('compose.index'))
