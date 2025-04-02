from json import load
from requests import get
from os import replace, startfile
from time import sleep
from sys import executable
class Updater:
    def __init__(self):
        with open("app_info.json", "r") as file:
            temp = load(file)
            self.version = temp["version"]
            self.origin = temp["origin"]

    def check_for_updates(self):
        url = f"https://api.github.com/repos/{self.origin}/releases/latest"
        try:
            response = get(url)
            if response.status_code == 200:
                release = response.json()
                latest_version = release["tag_name"]
                if latest_version > self.version:
                    print(f"New version available: {latest_version}")
                    for asset in release["assets"]:
                        if asset["name"].endswith(".exe"):
                            return asset["browser_download_url"]
            else:
                print(f"Error fetching release info: {response.status_code}")
        except Exception as e:
            print(f"Error checking for updates: {e}")
        return None

    def download_update(self, download_url: str, temp_path: str):
        print(f"Downloading update from {download_url}...")
        response = get(download_url, stream=True)
        with open(temp_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print("Download complete.")
    
    def replace_and_restart(self, temp_path: str, current_path: str):
        print("Replacing old version with new version...")
        sleep(2)
        replace(temp_path, current_path)
        print('Update complete. Restarting application...')
        startfile(current_path)
    
    def run_update(self, download_url: str):
        temp_path = executable + ".new"
        self.download_update(download_url, temp_path)
        self.replace_and_restart(temp_path, executable)
