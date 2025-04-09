from json import load
from requests import get
from packaging import version
from os import path
from sys import argv, exit
from subprocess import run, DETACHED_PROCESS
from src.config_system.utility import Utility



class Updater:
    def __init__(self):
        with open("app_info.json", "r") as f:
            self.info = load(f)
        self.url = f"https://api.github.com/repos/{self.__get_origin()}/releases/latest"

    def __get_latest_version(self):
        try:
            response = get(self.url)
            response.raise_for_status()
            data = response.json()
            latest_version = data["tag_name"]
            return latest_version
        except Exception as e:
            print(f"Error fetching version: {e}")
            return None

    def __get_current_version(self):
        return self.info["version"]

    def __get_origin(self):
        return self.info["origin"]

    def __is_update_available(self):
        try:
            latest_version = self.__get_latest_version()
            if latest_version:
                current_version = self.__get_current_version()
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
    
    def __build_bat(self, current_executable, new_executable : str) -> str:
        temp_dir = Utility.get_temp_directory()
        backup_executable = path.join(current_executable + ".backup")
        bat_path = path.join(temp_dir, "update_script.bat")

        bat_script = f"""@echo off
timeout /t 1 /nobreak >nul
del "{backup_executable}" 2 >nul
ren "{current_executable}" "{path.basename(backup_executable)}"
copy "{new_executable}" "{current_executable}"
start "" "{current_executable}" --no_update
del "{new_executable}"
del "{bat_path}"
"""
        
        with open(bat_path, "w") as bat_file:
            bat_file.write(bat_script)
        return bat_path


    def __download_update(self):
        try:
            response = get(self.url)
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
                file_name = path.join(
                    temp_dir, f"DataTransferApp_update_{data['tag_name']}.exe")

                print(f"Downloading update to {file_name}...")

                with get(download_url, stream=True) as r:
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
    
    def run_updater(self, current_executable) -> None:
        try:
            if self.__is_update_available():
                print('Update available')
                file_name = self.__download_update()
                if file_name:
                    bat_path = self.__build_bat(current_executable, file_name)
                    print(f"Running update script: {bat_path}")
                    command = f'Start-Process -FilePath "{bat_path}" -Verb RunAs'
                    run(["powershell", "-Command", command], shell=True, creationflags=DETACHED_PROCESS)
                    exit(0)
                    return True
        except Exception as e:
            print(f"Error in updater: {e}")
            return False
    
    def cleanup(self) -> None:
        try:
            temp_dir = Utility.get_temp_directory()
            bat_path = path.join(temp_dir, "update_script.bat")
            if path.exists(bat_path):
                path.remove(bat_path)
                print(f"Removed temporary file: {bat_path}")
        except Exception as e:
            print(f"Error cleaning up: {e}")

