from flet.core.file_picker import FilePickerFileType
from flet.core.icon_button import IconButton
from flet.core.image import Image
from src.config_system.utility import Utility
from src.config_system.config_service import ConfigService


class Buttons:
    def __init__(self) -> None:
        self.config_path = Utility.get_config_path()

    @staticmethod
    def _icon_asset(asset_path: str, size: int) -> Image:
        return Image(src=asset_path, width=size, height=size)

    def registry_file_picker_button(self, handler) -> IconButton:
        return IconButton(
            content=self._icon_asset("settings.svg", 24),
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
            content=self._icon_asset("settings.svg", 24),
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
            content=self._icon_asset("open_in_new.svg", 24),
            on_click=lambda _: Utility.start_file(
                ConfigService.static_read_config(self.config_path)["paths"]["registry_path"]),
            icon_size=24,
            disabled=disabled,
            tooltip="Открыть реестр"
        )

    def open_declaration_file_button(self, disabled) -> IconButton:
        return IconButton(
            content=self._icon_asset("open_in_new.svg", 24),
            on_click=lambda _: Utility.start_file(
                ConfigService.static_read_config(self.config_path)["paths"]["declaration_path"]),
            icon_size=24,
            disabled=disabled,
            tooltip="Открыть декларацию"
        )

    def excel_editor_button(self, handler) -> IconButton:
        return IconButton(
            content=self._icon_asset("edit_document.svg", 50),
            on_click=handler,
            icon_size=50,
            tooltip="Конфигуратор"
        )

    def transfer_button(self, handler, disabled) -> IconButton:
        return IconButton(
            content=self._icon_asset("merge_type.svg", 50),
            on_click=handler,
            icon_size=50,
            disabled=disabled,
            tooltip="Запустить перенос"
        )
