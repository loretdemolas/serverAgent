#serverAgent/home/routes.py
from flask import Flask, render_template, request, redirect, url_for
import docker
client = docker.from_env()

from . import home_blueprint

# Mockup data for active containers
active_containers = client.containers.list()

@home_blueprint.route('/')
def root():
    return redirect(url_for('home.index'))

@home_blueprint.route('/home')
def index():
    return render_template('home/home.html', containers=active_containers)

@home_blueprint.route('/start/<container_id>', methods=['POST'])
def start_container(container_id):
    container = client.containers.get(container_id)
    container.start()
    return redirect(url_for('home'))

@home_blueprint.route('/stop/<container_id>', methods=['POST'])
def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    return redirect(url_for('home'))

@home_blueprint.route('/restart/<container_id>', methods=['POST'])
def restart_container(container_id):
    container = client.containers.get(container_id)
    container.restart()
    return redirect(url_for('home'))

@home_blueprint.route('/logs/<container_id>')
def container_logs(container_id):
    container = client.containers.get(container_id)
    logs = container.logs().decode('utf-8')
    return render_template('logs.html', container_name=container.name, logs=logs)

@home_blueprint.route('/additional-content/<container_id>')
def additional_content(container_id):
    # Placeholder for additional content
    return render_template('additional_content.html')
