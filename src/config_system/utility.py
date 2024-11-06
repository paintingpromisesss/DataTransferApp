from os import path, getenv, startfile
from time import sleep


class Utility:
    @staticmethod
    def get_config_directory() -> str:
        return path.join(getenv("USERPROFILE"), "Documents", "DataTransfer Config")

    @staticmethod
    def get_config_path() -> str:
        return path.join(Utility.get_config_directory(), "config.json")

    @staticmethod
    def get_temp_directory() -> str:
        return getenv("TEMP")

    @staticmethod
    def get_temp_path() -> str:
        return path.normpath(path.join(Utility.get_temp_directory(), "declaration.xlsx"))

    @staticmethod
    def get_desktop_directory() -> str:
        return path.normpath(path.join(getenv("USERPROFILE"), "Desktop"))

    @staticmethod
    def start_file(filepath: str) -> None:
        startfile(filepath)

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
