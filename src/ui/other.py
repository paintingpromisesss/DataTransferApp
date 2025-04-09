from flet import Container, ProgressRing, colors, Page, alignment, AlertDialog, ElevatedButton, Text


class Other:
    def __init__(self, page: Page) -> None:
        self.page = page

    def progress_ring(self) -> Container:
        return Container(content=ProgressRing(),
                         bgcolor=colors.with_opacity(0.5, colors.BLACK),
                         width=self.page.width,
                         height=self.page.height,
                         visible=False,
                         alignment=alignment.center)

    def opening_dialog(self, handler) -> AlertDialog:
        return AlertDialog(
            title=Text("Перенос завершён"),
            content=Text(
                'После нажатия на кнопку "Открыть" будет открыт временный Excel файл. Позже его можно будет сохранить'),
            actions=[
                ElevatedButton(text="Открыть", on_click=lambda _: handler()),
            ]
        )

    def saving_dialog(self, handler) -> AlertDialog:
        return AlertDialog(
            title=Text("Сохранение"),
            content=Text(
                'Если все данные в порядке, нажмите "Сохранить", иначе - "Отменить"'),
            actions=[
                ElevatedButton(text="Сохранить",
                               on_click=lambda e: handler(e)),
                ElevatedButton(text="Отменить", on_click=lambda e: handler(e)),
            ]
        )

    @staticmethod
    def error_dialog(error_dialog_handler) -> AlertDialog:
        return AlertDialog(
            title=Text("Произошла ошибка"),
            content=Text(""),
            actions=[
                ElevatedButton(
                    text="Ок", on_click=lambda e: error_dialog_handler(e))
            ]
        )
