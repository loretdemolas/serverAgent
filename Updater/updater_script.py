# updater_script.py
import requests
import json

def fetch_latest_approved_updates(github_repo):
    try:
        # Fetch the latest approved updates list from GitHub
        response = requests.get(f"https://raw.githubusercontent.com/{github_repo}/main/Core/approved_updates.json")

        if response.status_code == 200:
            # Update the internal database with the latest approved updates list
            with open("Core/approved_updates.json", "w") as file:
                file.write(response.text)
            print("Updater: Updated approved updates successfully.")
        else:
            print(f"Updater: Failed to fetch approved updates. Status code: {response.status_code}")

    except Exception as e:
        print(f"Updater: Error fetching approved updates: {e}")

# GitHub repository information
github_repo = "your_username/your_repo"

# Fetch the latest approved updates
fetch_latest_approved_updates(github_repo)
