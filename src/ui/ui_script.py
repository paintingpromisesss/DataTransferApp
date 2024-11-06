from flet import Page, FilePicker, Row, Column, NavigationBar, NavigationBarDestination, icons, Text, Container, alignment, FilePickerResultEvent, FilePickerFileType
from src.app.app import App
from src.config_system.utility import Utility
from src.ui.fields import Fields
from src.ui.buttons import Buttons
from src.ui.other import Other
from atexit import register
from time import sleep


class UIScript:
    def __init__(self, default_page: Page) -> None:
        self.page = default_page
        self.page.title = "Перенос данных"
        self.page.window.width = 490
        self.page.window.height = 400
        self.page.window_resizable = False
        self.page.window.icon = "D:/Programming/DataTransferRework/assets/icon.ico"

        self.app = App()
        self.config = self.app.read_config()
        self.fields = Fields(self.config)
        self.buttons = Buttons()
        self.other = Other(self.page)

        self.error_dialog = self.other.error_dialog(self.error_dialog_handler)

        self.registry_path_field = self.fields.registry_path_field()
        self.declaration_path_field = self.fields.declaration_path_field()

        self.registry_article_field = self.fields.registry_article_field(
            self.registry_article_field_handler)
        self.declaration_article_field = self.fields.declaration_article_field(
            self.declaration_article_field_handler)

        self.registry_start_row_field = self.fields.registry_start_row_field(
            self.registry_start_row_field_handler)
        self.declaration_start_row_field = self.fields.declaration_start_row_field(
            self.declaration_start_row_field_handler)

        self.registry_file_picker = FilePicker(
            on_result=self.registry_file_picker_handler)
        self.declaration_file_picker = FilePicker(
            on_result=self.declaration_file_picker_handler)

        self.declaration_file_saver = FilePicker(
            on_result=self.declaration_file_saver_handler)

        self.progress_ring = self.other.progress_ring()

        self.opening_dialog = self.other.opening_dialog(
            self.opening_dialog_handler)
        self.saving_dialog = self.other.saving_dialog(
            self.saving_dialog_handler)

        self.open_registry_file_button = self.buttons.open_registry_file_button()
        self.open_declaration_file_button = self.buttons.open_declaration_file_button()

        self.registry_file_picker_button = self.buttons.registry_file_picker_button(
            self.registry_file_picker)
        self.declaration_file_picker_button = self.buttons.declaration_file_picker_button(
            self.declaration_file_picker)

        self.excel_editor_button = self.buttons.excel_editor_button(
            self.excel_editor_button_handler)
        self.transfer_button = self.buttons.transfer_button(
            self.transfer_button_handler)

        self.registry_funcs_row = Row(
            [
                self.registry_path_field,
                self.registry_file_picker_button,
                self.open_registry_file_button
            ], spacing=10
        )

        self.declaration_funcs_row = Row(
            [
                self.declaration_path_field,
                self.declaration_file_picker_button,
                self.open_declaration_file_button
            ]
        )

        self.article_settings_column = Column(
            [Row([self.registry_article_field, self.registry_start_row_field], spacing=13),
             Row([self.declaration_article_field, self.declaration_start_row_field], spacing=13)],
            spacing=13
        )

        self.page.overlay.extend([self.registry_file_picker, self.declaration_file_picker,
                                 self.declaration_file_saver, self.progress_ring, self.opening_dialog, self.saving_dialog, self.error_dialog])

        self.page.navigation_bar = NavigationBar(
            destinations=[
                NavigationBarDestination(
                    label="Перенос", icon=icons.MERGE_TYPE),
                NavigationBarDestination(
                    label="Настройки", icon=icons.DISPLAY_SETTINGS)
            ],
            on_change=self.navigation_bar_handler,
            selected_index=0)

        self.show_transfer_page()

        register(self.close_app)

    @staticmethod
    def error_handler(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.error_dialog.content = Text(f"Произошла непредвиденная ошибка: {e}.")
                self.error_dialog.open = True
                self.page.update()

        return wrapper

    @error_handler
    def show_transfer_page(self) -> None:
        self.page.controls.clear()
        config_data = self.app.read_config()
        self.registry_path_field.value = config_data["paths"]["registry_path"]
        self.declaration_path_field.value = config_data["paths"]["declaration_path"]
        content = Column([Column([self.registry_funcs_row, self.declaration_funcs_row]), Container(
            content=self.transfer_button, alignment=alignment.center, width=self.page.width)], spacing=50)
        self.page.add(content)

    @error_handler
    def show_settings_page(self) -> None:
        self.page.controls.clear()
        config_data = self.app.read_config()
        self.registry_article_field.value = config_data["article_data"]["registry_article_key"]
        self.declaration_article_field.value = config_data["article_data"]["declaration_article_key"]
        self.registry_start_row_field.value = config_data["start_rows"]["registry_start_row"]
        self.declaration_start_row_field.value = config_data["start_rows"]["declaration_start_row"]
        content = Column([self.article_settings_column, Container(
            content=self.excel_editor_button, alignment=alignment.center, width=self.page.width)], spacing=50)
        self.page.add(content)

    @error_handler
    def navigation_bar_handler(self, e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            self.show_transfer_page()
        elif selected_index == 1:
            self.show_settings_page()

    @error_handler
    def registry_article_field_handler(self, e=None) -> None:
        current_value = self.registry_article_field.value
        while not current_value:
            sleep(1)
        else:
            self.app.edit_registry_article_key(current_value)

    @error_handler
    def declaration_article_field_handler(self, e=None) -> None:
        current_value = self.declaration_article_field.value
        while not current_value:
            sleep(1)
        else:
            self.app.edit_declaration_article_key(current_value)

    @error_handler
    def registry_start_row_field_handler(self, e=None) -> None:
        current_value = self.registry_start_row_field.value
        while not current_value:
            sleep(1)
        else:
            self.app.edit_registry_start_row(int(current_value))

    @error_handler
    def declaration_start_row_field_handler(self, e=None) -> None:
        current_value = self.declaration_start_row_field.value
        while not current_value:
            sleep(1)
        else:
            self.app.edit_declaration_start_row(int(current_value))

    @error_handler
    def registry_file_picker_handler(self, e: FilePickerResultEvent) -> None:
        if e.files:
            selected_file = e.files[0].path
            self.app.edit_registry_path(selected_file)
            self.registry_path_field.value = selected_file
            self.page.update()

    @error_handler
    def declaration_file_picker_handler(self, e: FilePickerResultEvent) -> None:
        if e.files:
            selected_file = e.files[0].path
            self.app.edit_declaration_path(selected_file)
            self.declaration_path_field.value = selected_file
            self.page.update()

    @error_handler
    def declaration_file_saver_handler(self, e: FilePickerResultEvent) -> None:
        save_location = e.path
        if save_location:
            self.show_loading_overlay(True)
            self.app.save_temp_declaration(save_location)
            self.app.delete_temp_declaration()
            self.show_loading_overlay(False)

    @error_handler
    def opening_dialog_handler(self, e=None) -> None:
        self.app.open_temp_declaration()
        if Utility.is_file_closed(Utility.get_temp_path()):
            self.page.close(self.opening_dialog)
            self.page.open(self.saving_dialog)
            self.page.update()

    @error_handler
    def saving_dialog_handler(self, e) -> None:
        if e.control.text == "Сохранить":
            self.declaration_file_saver.save_file(dialog_title="Сохранение",
                                                  initial_directory=Utility.get_desktop_directory(),
                                                  file_name="Декларация.xlsx",
                                                  file_type=FilePickerFileType.CUSTOM,
                                                  allowed_extensions=["xlsx"])
            self.page.close(self.saving_dialog)
            self.page.update()
        else:
            self.app.delete_temp_declaration()
            self.page.close(self.saving_dialog)
            self.page.update()

    @error_handler
    def excel_editor_button_handler(self, e=None) -> None:
        self.progress_ring.visible = True
        self.page.update()
        self.app.start_excel_configurator()
        self.progress_ring.visible = False
        self.page.update()

    @error_handler
    def show_loading_overlay(self, show) -> None:
        self.progress_ring.visible = show
        self.page.update()

    @error_handler
    def transfer_button_handler(self, e=None) -> None:
        self.show_loading_overlay(True)
        self.app.transfer()
        self.show_loading_overlay(False)
        self.opening_dialog.open = True
        self.page.update()

    @error_handler
    def error_dialog_handler(self, e):
        if e.control.text == "Ок":
            self.error_dialog.open = False
            if self.progress_ring.visible is True:
                self.show_loading_overlay(False)
            self.page.update()

    @error_handler
    def close_app(self) -> None:
        try:
            self.app.delete_temp_excel_file()
        except Exception:
            pass
        try:
            self.app.delete_temp_declaration()
        except Exception:
            pass