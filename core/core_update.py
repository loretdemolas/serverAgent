# core/core_update.py
import os
import subprocess
import requests
import hashlib

class CoreUpdater:
    @staticmethod
    def update_core(github_repo, latest_version):
        try:
            # Download the latest release asset (Docker Compose configuration)
            download_url = f"https://github.com/{github_repo}/releases/download/{latest_version}/docker-compose.yml"
            response = requests.get(download_url)

            if response.status_code == 200:
                # Save the downloaded Docker Compose configuration
                with open("docker-compose.yml", "w") as file:
                    file.write(response.text)

                # Verify the integrity of the downloaded file
                if CoreUpdater.verify_checksum("docker-compose.yml", latest_version):
                    # Restart the Docker containers with the updated configuration
                    subprocess.run(["docker-compose", "down"])
                    subprocess.run(["docker-compose", "up", "-d"])

                    print(f"Core updated to version {latest_version}")
                else:
                    print("Checksum verification failed. Aborting update.")
            else:
                print(f"Failed to download Docker Compose configuration. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error updating core: {e}")
        finally:
            # Cleanup temporary files
            os.remove("docker-compose.yml")

    @staticmethod
    def verify_checksum(file_path, expected_checksum):
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as file:
            # Read the file in chunks to handle large files
            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)

        actual_checksum = sha256.hexdigest()
        return actual_checksum == expected_checksum
