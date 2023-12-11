# core/core_agent.py
import time
import json
from core.addon_interface import AddonInterface
from core.core_update import CoreUpdater

class CoreAgent:
    def __init__(self, github_repo):
        self.addons = []
        self.github_repo = github_repo
        self.internal_database_path = 'approved_updates.json'
        self.internal_database = self.load_internal_database()
        self.installed_addons_path = 'installed_addons.json'
        self.installed_addons = self.load_installed_addons()

    def load_internal_database(self):
        try:
            with open(self.internal_database_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Internal database not found. Creating a new one.")
            return {"updates": []}

    def load_installed_addons(self):
        try:
            with open(self.installed_addons_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Installed addons database not found. Creating a new one.")
            return {"addons": []}

    def save_installed_addons(self):
        with open(self.installed_addons_path, 'w') as file:
            json.dump(self.installed_addons, file)

    def register_addon(self, addon):
        if isinstance(addon, AddonInterface):
            self.addons.append(addon)
        else:
            print("Error: Attempting to register an addon that doesn't implement the AddonInterface.")

    def apply_addons(self):
        for addon in self.addons:
            addon.apply(self.installed_addons)
    
    def update_core(self, latest_version):
        CoreUpdater.update_core(self.github_repo, latest_version)

    def start(self):
        while True:
            self.apply_addons()
            self.save_installed_addons()  # Save the installed addons after applying updates
            time.sleep(60)  # Adjust the interval as needed
