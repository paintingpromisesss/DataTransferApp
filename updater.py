import json
import requests
from packaging import version
import os
from src.config_system.utility import Utility
import sys
import subprocess


class Updater:
    def __init__(self):
        with open("app_info.json", "r") as f:
            self.info = json.load(f)
            self.url = f"https://api.github.com/repos/{self._get_origin()}/releases/latest"

    def _get_latest_version(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            latest_version = data["tag_name"]
            return latest_version
        except Exception as e:
            print(f"Error fetching version: {e}")
            return None

    def _get_current_version(self):
        return self.info["version"]

    def _get_origin(self):
        return self.info["origin"]

    def _is_update_available(self):
        try:
            latest_version = self._get_latest_version()
            if latest_version:
                current_version = self._get_current_version()
                if version.parse(latest_version) > version.parse(current_version):
                    return True
                else:
                    return False
            else:
                print("Could not fetch the latest version.")
                return False
        except Exception as e:
            print(f"Error comparing versions: {e}")
            return False

    def _download_update(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()
            download_url = None
            if Utility.get_os_type() == "Windows":
                for asset in data["assets"]:
                    if asset["name"].endswith(".exe"):
                        download_url = asset["browser_download_url"]
                        break
            elif Utility.get_os_type() == "Linux":
                for asset in data["assets"]:
                    if asset["name"].endswith(".bin"):
                        download_url = asset["browser_download_url"]
                        break
            if download_url:

                temp_dir = Utility.get_temp_directory()
                file_name = os.path.join(
                    temp_dir, f"DataTransferApp_update_{data['tag_name']}.exe")

                # Download the file
                print(f"Downloading update to {file_name}...")

                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                print(f"Update downloaded to {file_name}")
                return file_name
            else:
                print("No executable found in the release assets.")
                return None

        except Exception as e:
            print(f"Error downloading update: {e}")
            return None
