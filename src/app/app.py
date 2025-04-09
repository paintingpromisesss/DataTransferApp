from src.config_system.config_service import ConfigService
from src.config_system.excel_configurator import ExcelConfigurator
from src.transfer_system.transfer_service import TransferService


class App:
    def __init__(self) -> None:
        self.config_service = ConfigService()
        self.transfer_service = TransferService()
        self.excel_configurator = ExcelConfigurator()

    def read_config(self):
        return self.config_service.read_config()

    def edit_registry_path(self, new_registry_path: str) -> None:
        self.config_service.edit_registry_path(new_registry_path)

    def edit_declaration_path(self, new_declaration_path: str) -> None:
        self.config_service.edit_declaration_path(new_declaration_path)

    def edit_registry_article_key(self, new_registry_article_key: str) -> None:
        self.config_service.edit_registry_article_key(
            new_registry_article_key)

    def edit_declaration_article_key(self, new_declaration_article_key: str) -> None:
        self.config_service.edit_declaration_article_key(
            new_declaration_article_key)

    def edit_registry_start_row(self, new_registry_start_row: int) -> None:
        self.config_service.edit_registry_start_row(new_registry_start_row)

    def edit_declaration_start_row(self, new_declaration_start_row: int) -> None:
        self.config_service.edit_declaration_start_row(
            new_declaration_start_row)

    def start_excel_configurator(self) -> None:
        self.excel_configurator.open_excel_configurator()

    def delete_temp_excel_file(self) -> None:
        self.excel_configurator.delete_temp_file()

    def transfer(self) -> None:
        self.transfer_service.transfer()

    def open_temp_declaration(self) -> None:
        self.transfer_service.open_temp_declaration()

    def delete_temp_declaration(self) -> None:
        self.transfer_service.delete_temp_declaration()

    def save_temp_declaration(self, save_path: str) -> None:
        self.transfer_service.save_temp_declaration(save_path)
