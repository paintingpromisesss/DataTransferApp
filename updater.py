from json import load
from requests import get
from packaging import version
from os import path
from sys import exit
from subprocess import run, DETACHED_PROCESS
from src.config_system.utility import Utility


class Updater:
    def __init__(self):
        base_dir = path.dirname(path.abspath(__file__))
        app_info_path = path.join(base_dir, "app_info.json")
        with open(app_info_path, "r") as f:
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

    def __build_ps1(self, current_executable, new_executable: str) -> str:
        temp_dir = Utility.get_temp_directory()
        backup_executable = path.join(current_executable + ".backup")
        ps1_path = path.join(temp_dir, "update_script.ps1")

        ps1_script = f"""chcp 65001
Start-Sleep -Seconds 1
Remove-Item -Path "{backup_executable}" -ErrorAction SilentlyContinue
Rename-Item -Path "{current_executable}" -NewName "{path.basename(backup_executable)}"
Copy-Item -Path "{new_executable}" -Destination "{current_executable}"
Start-Process -FilePath "{current_executable}" -ArgumentList "--no_update" -NoNewWindow
Remove-Item -Path "{new_executable}"
Remove-Item -Path "{ps1_path}"
"""

        with open(ps1_path, "w") as ps1_file:
            ps1_file.write(ps1_script)
        return ps1_path

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
                    ps1_path = self.__build_ps1(current_executable, file_name)
                    print(f"Running update script: {ps1_path}")
                    command = f'Start-Process -FilePath "powershell" -ArgumentList "-ExecutionPolicy Bypass -File {ps1_path}" -Verb RunAs'
                    run(["powershell", "-Command", command],
                        shell=True, creationflags=DETACHED_PROCESS)
                    exit(0)
                    return True
        except Exception as e:
            print(f"Error in updater: {e}")
            return False
