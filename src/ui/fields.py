from flet import TextField, TextStyle, TextCapitalization, InputFilter, NumbersOnlyInputFilter


class Fields:
    def __init__(self, config: dict) -> None:
        self.config = config

    def registry_path_field(self) -> TextField:
        return TextField(
            label="Путь к реестру", read_only=True, width=350,
            value=self.config["paths"]["registry_path"], text_style=TextStyle(
                size=12)
        )

    def declaration_path_field(self) -> TextField:
        return TextField(
            label="Путь к декларации", read_only=True, width=350,
            value=self.config["paths"]["declaration_path"], text_style=TextStyle(
                size=12)
        )

    def registry_article_field(self, handler) -> TextField:
        return TextField(
            adaptive=True, label="Буква артикула в реестре", value=self.config["article_data"]["registry_article_key"], width=220,
            text_style=TextStyle(size=12), capitalization=TextCapitalization.CHARACTERS,
            input_filter=InputFilter(allow=True, regex_string=r"[A-Za-z]|^$"),
            on_change=lambda _: handler()
        )

    def declaration_article_field(self, handler) -> TextField:
        return TextField(
            label="Буква артикула в декларации", value=self.config["article_data"]["declaration_article_key"], width=220,
            text_style=TextStyle(size=12), capitalization=TextCapitalization.CHARACTERS,
            input_filter=InputFilter(allow=True, regex_string=r"[A-Za-z]|^$"),
            on_change=lambda _: handler()
        )

    def registry_start_row_field(self, handler) -> TextField:
        return TextField(
            adaptive=True, label="Стартовая строка в реестре", value=self.config["start_rows"]["registry_start_row"], width=220,
            text_style=TextStyle(size=12), input_filter=NumbersOnlyInputFilter(),
            on_change=lambda _: handler()
        )

    def declaration_start_row_field(self, handler) -> TextField:
        return TextField(
            adaptive=True, label="Стартовая строка в декларации", value=self.config["start_rows"]["declaration_start_row"], width=220,
            text_style=TextStyle(size=12), input_filter=NumbersOnlyInputFilter(),
            on_change=lambda _: handler()
        )
