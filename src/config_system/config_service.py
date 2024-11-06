from os import path, makedirs
from json import dump, load
from src.config_system.utility import Utility

template = {
    "paths": {
        "registry_path": "",
        "declaration_path": ""
    },
    "article_data": {
        "registry_article_key": "",
        "declaration_article_key": ""
    },
    "start_rows": {
        "registry_start_row": "",
        "declaration_start_row": ""
    },
    "transfer_pairs": {}
}


class ConfigService:
    def __init__(self) -> None:
        config_directory = Utility.get_config_directory()
        self.config_path = Utility.get_config_path()
        if not path.exists(config_directory):
            makedirs(config_directory)
        if not path.exists(self.config_path):
            self.write_config(template)

    def read_config(self) -> dict:
        with open(self.config_path, "r") as file:
            return load(file)

    def write_config(self, edited_config: dict) -> None:
        with open(self.config_path, "w") as file:
            dump(edited_config, file, indent=4)

    def edit_transfer_pairs(self, edited_config: dict) -> None:
        self.write_config(edited_config)

    @staticmethod
    def static_read_config(config_path: str) -> dict:
        with open(config_path, "r") as file:
            return load(file)

    @staticmethod
    def static_write_config(config_path: str, edited_config: dict) -> None:
        with open(config_path, "w") as file:
            dump(edited_config, file, indent=4)

    @staticmethod
    def static_edit_transfer_pairs(config_path: str, edited_config: dict) -> None:
        ConfigService.static_write_config(config_path, edited_config)

    def edit_registry_path(self, new_registry_path: str) -> None:
        config_data = self.read_config()
        config_data["paths"]["registry_path"] = new_registry_path
        self.write_config(config_data)

    def edit_declaration_path(self, new_declaration_path: str) -> None:
        config_data = self.read_config()
        config_data["paths"]["declaration_path"] = new_declaration_path
        self.write_config(config_data)

    def edit_registry_article_key(self, new_registry_article_key: str) -> None:
        config_data = self.read_config()
        if new_registry_article_key != "":
            config_data["article_data"]["registry_article_key"] = new_registry_article_key
            self.write_config(config_data)

    def edit_declaration_article_key(self, new_declaration_article_key: str) -> None:
        config_data = self.read_config()
        if new_declaration_article_key != "":
            config_data["article_data"]["declaration_article_key"] = new_declaration_article_key
            self.write_config(config_data)

    def edit_registry_start_row(self, new_registry_start_row: int) -> None:
        config_data = self.read_config()
        if new_registry_start_row != "":
            config_data["start_rows"]["registry_start_row"] = new_registry_start_row
            self.write_config(config_data)

    def edit_declaration_start_row(self, new_declaration_start_row: int) -> None:
        config_data = self.read_config()
        if new_declaration_start_row != "":
            config_data["start_rows"]["declaration_start_row"] = new_declaration_start_row
            self.write_config(config_data)