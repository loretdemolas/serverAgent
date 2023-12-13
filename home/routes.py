#serverAgent/home/routes.py
from flask import Flask, render_template, Blueprint, redirect, url_for, request
import docker
from flask_socketio import emit
client = docker.from_env()

from . import home_blueprint, socketio

additional_content_blueprint = Blueprint('additional_content', __name__)

# Mockup data for active containers
active_containers = client.containers.list(all=True)

@home_blueprint.route('/')
def root():
    return redirect(url_for('home.index'))

@home_blueprint.route('/home')
def index():
    active_containers = client.containers.list(all=True)
    return render_template('home/home.html', containers=active_containers)

@home_blueprint.route('/start/<container_id>', methods=['POST'])
def start_container(container_id):
    container = client.containers.get(container_id)
    container.start()
    active_containers = client.containers.list(all=True)
    return redirect(url_for('home.root', containers=active_containers))

@home_blueprint.route('/stop/<container_id>', methods=['POST'])
def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    active_containers = client.containers.list(all=True)
    return redirect(url_for('home.root', containers=active_containers))

@home_blueprint.route('/restart/<container_id>', methods=['POST'])
def restart_container(container_id):
    container = client.containers.get(container_id)
    container.restart()
    active_containers = client.containers.list(all=True)
    return redirect(url_for('home.root', containers=active_containers))

@home_blueprint.route('/logs/<container_id>')
def container_logs(container_id):
    container = client.containers.get(container_id)

    def log_generator(container):
        for line in container.logs(stream=True, follow=True):
            # Send each log line to the client
            emit('log', {'line': line.decode('utf-8')})

    # Start a separate thread to stream logs while rendering the template
    socketio.start_background_task (log_generator)

    return render_template('logs.html', container_name=container.name)

@additional_content_blueprint.route('/additional-content')
def additional_content():
    container_id = request.args.get('container_id')
    # Get container details
    container = client.containers.get(container_id)

    # Get resource usage
    stats = container.stats(stream=False)
    cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
    memory_usage = stats['memory_stats']['usage']

    # Get container configuration
    command = container.attrs['Config']['Cmd']
    environment_variables = container.attrs['Config']['Env']
    exposed_ports = container.attrs['Config']['ExposedPorts']
    volumes = container.attrs['Config']['Volumes']

    # Get network information
    ip_address = container.attrs['NetworkSettings']['IPAddress']
    port_bindings = container.attrs['HostConfig']['PortBindings']

    # Get health status
    health_status = container.attrs['State'].get('Health', {}).get('Status', 'N/A')
    last_health_check_result = container.attrs['State'].get('Health', {}).get('Log', [])
    last_health_check_result = last_health_check_result[-1]['Output'] if last_health_check_result else 'N/A'


    # Get labels and metadata
    labels = container.labels
    metadata = container.attrs.get('Metadata', {})

    # Render the template with the container information
    return render_template('additional_content.html',
                           container_name=container.name,
                           container_id=container.short_id,
                           container_image=container.image.tags[0],
                           container_status=container.status,
                           container_created_time=container.attrs['Created'],
                           container_cpu_usage=cpu_usage,
                           container_memory_usage=memory_usage,
                           container_command=command,
                           container_env_vars=environment_variables,
                           container_exposed_ports=exposed_ports,
                           container_volumes=volumes,
                           container_ip_address=ip_address,
                           container_port_bindings=port_bindings,
                           container_health_status=health_status,
                           last_health_check_result=last_health_check_result,
                           container_labels=labels,
                           container_metadata=metadata
                           )
