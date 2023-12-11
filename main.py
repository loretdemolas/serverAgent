# main.py
from core.core_agent import CoreAgent
from core.addon_interface import AddonInterface
from core.update_interface import UpdateInterface
import os
import importlib.util
import json

# GitHub repository information
github_repo = "your_username/your_repo"

# Initialize the core agent with the GitHub repository
core_agent = CoreAgent(github_repo)

# Load the internal database to check for approved updates
internal_database_path = 'approved_updates.json'
try:
    with open(internal_database_path, 'r') as file:
        internal_database = json.load(file)
except FileNotFoundError:
    print(f"Error: Internal database file not found at {internal_database_path}. Exiting.")
    exit(1)

# Dynamically register approved updates
updates_path = 'updates'
for update_info in internal_database.get('updates', []):
    update_name = update_info.get('name')
    update_version = update_info.get('version')
    update_module_path = os.path.join(updates_path, f"{update_name.lower()}_{update_version}.py")

    if os.path.isfile(update_module_path):
        spec = importlib.util.spec_from_file_location(f"{update_name}_module", update_module_path)
        update_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(update_module)

        # Check if the loaded module implements the UpdateInterface
        if issubclass(update_module.UpdateClass, UpdateInterface):
            # Instantiate the update class and apply it
            update_instance = update_module.UpdateClass()
            update_instance.apply(core_agent)
        else:
            print(f"Error: Update {update_name} does not implement the UpdateInterface. Skipping application.")
    else:
        print(f"Error: Update module not found at {update_module_path}. Skipping application.")

# Register addons dynamically
addons_path = 'addons'
for addon_info in core_agent.installed_addons.get('addons', []):
    addon_name = addon_info.get('name')
    addon_version = addon_info.get('version')
    addon_module_path = os.path.join(addons_path, f"{addon_name.lower()}_{addon_version}.py")

    if os.path.isfile(addon_module_path):
        spec = importlib.util.spec_from_file_location(f"{addon_name}_module", addon_module_path)
        addon_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(addon_module)

        # Check if the loaded module implements the AddonInterface
        if issubclass(addon_module.AddonClass, AddonInterface):
            # Instantiate the addon class and register it with the core agent
            addon_instance = addon_module.AddonClass()
            core_agent.register_addon(addon_instance)
        else:
            print(f"Error: Addon {addon_name} does not implement the AddonInterface. Skipping registration.")
    else:
        print(f"Error: Addon module not found at {addon_module_path}. Skipping registration.")

# Start the core agent
core_agent.start()
