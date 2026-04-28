from os import path, getenv, name
from sys import argv, executable
import sys
from time import sleep
from subprocess import run

errors = {
    "ValueError": "Стартовые строки в реестре и/или декларации указаны неверно"
}


class Utility:
    @staticmethod
    def get_program_directory() -> str:
        program_path = executable if getattr(sys, "frozen", False) else argv[0]
        return path.dirname(path.abspath(program_path))

    @staticmethod
    def get_app_directory() -> str:
        return path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

    @staticmethod
    def get_assets_directory() -> str:
        return path.join(Utility.get_app_directory(), "assets")

    @staticmethod
    def get_asset_path(filename: str) -> str:
        return path.join(Utility.get_assets_directory(), filename)

    @staticmethod
    def get_config_directory() -> str:
        match Utility.get_os_type():
            case "Windows":
                return path.join(getenv("USERPROFILE"), "Documents", "DataTransfer Config")
            case "Linux":
                return path.join(getenv("HOME"), ".config", "DataTransfer Config")

    @staticmethod
    def get_config_path() -> str:
        return path.join(Utility.get_config_directory(), "config.json")

    @staticmethod
    def get_temp_directory() -> str:
        match Utility.get_os_type():
            case "Windows":
                return path.join(getenv("USERPROFILE"), "AppData", "Local", "Temp")
            case "Linux":
                return path.join("/tmp")

    @staticmethod
    def get_temp_path() -> str:
        return path.normpath(path.join(Utility.get_temp_directory(), "declaration.xlsx"))

    @staticmethod
    def get_desktop_directory() -> str:
        match Utility.get_os_type():
            case "Windows":
                return path.normpath(path.join(getenv("USERPROFILE"), "Desktop"))
            case "Linux":
                return path.normpath(path.join(getenv("HOME"), "Desktop"))

    @staticmethod
    def get_os_type() -> str:
        if name == "nt":
            return "Windows"
        elif name == "posix":
            return "Linux"

    @staticmethod
    def start_file(filepath: str) -> None:
        match Utility.get_os_type():
            case "Windows":
                from os import startfile
                startfile(filepath)
            case "Linux":
                run(["xdg-open", filepath], check=True)

    @staticmethod
    def is_file_closed(filepath: str) -> bool:
        flag = False
        sleep(3)
        while not flag:
            sleep(0.5)
            try:
                with open(filepath, "r+"):
                    flag = True
            except IOError:
                pass
        return True
