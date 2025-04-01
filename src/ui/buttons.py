from flet import IconButton, icons, FilePickerFileType
from src.config_system.utility import Utility
from src.config_system.config_service import ConfigService
class Buttons:
    def __init__(self) -> None:
        self.config_path = Utility.get_config_path()
    def registry_file_picker_button(self, handler) -> IconButton:
        return IconButton(
            icon=icons.SETTINGS,
            on_click=lambda _: handler.pick_files(
                allow_multiple=False,
                file_type=FilePickerFileType.CUSTOM,
                allowed_extensions=["xlsx"]
            ),
            icon_size=24,
            tooltip="Изменить путь"
        )

    def declaration_file_picker_button(self, handler) -> IconButton:
        return IconButton(
            icon=icons.SETTINGS,
            on_click=lambda _: handler.pick_files(
                allow_multiple=False,
                file_type=FilePickerFileType.CUSTOM,
                allowed_extensions=["xlsx"]
            ),
            icon_size=24,
            tooltip="Изменить путь"
        )

    def open_registry_file_button(self, disabled) -> IconButton:
        return IconButton(
            icon=icons.OPEN_IN_NEW,
            on_click=lambda _: Utility.start_file(
                ConfigService.static_read_config(self.config_path)["paths"]["registry_path"]),
            icon_size=24,
            disabled=disabled,
            tooltip="Открыть реестр"
        )

    def open_declaration_file_button(self, disabled) -> IconButton:
        return IconButton(
            icon=icons.OPEN_IN_NEW,
            on_click=lambda _: Utility.start_file(
                ConfigService.static_read_config(self.config_path)["paths"]["declaration_path"]),
            icon_size=24,
            disabled=disabled,
            tooltip="Открыть декларацию"
        )
    def excel_editor_button(self, handler) -> IconButton:
        return IconButton(
            icon=icons.EDIT_DOCUMENT,
            on_click=handler,
            icon_size=50,
            tooltip="Конфигуратор"
        )

    def transfer_button(self, handler, disabled) -> IconButton:
        return IconButton(
            icon=icons.MERGE_TYPE,
            on_click=handler,
            icon_size=50,
            disabled=disabled,
            tooltip="Запустить перенос"
        )
