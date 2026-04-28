from logging import getLogger
from os import path, remove
from openpyxl import load_workbook
from src.config_system.config_service import ConfigService
from src.config_system.utility import Utility

logger = getLogger(__name__)


class TransferService:

    def __init__(self) -> None:
        self.config_path = Utility.get_config_path()
        self.path_to_temp_declaration = Utility.get_temp_path()

    @staticmethod
    def _normalize_article(article) -> str | None:
        if article is None:
            return None

        normalized_article = str(article).strip()
        if normalized_article == "":
            return None

        return normalized_article

    def transfer(self) -> None:
        logger.info("Начат перенос данных")
        config_data = ConfigService.static_read_config(self.config_path)
        registry_article_key = config_data["article_data"]["registry_article_key"]
        declaration_article_key = config_data["article_data"]["declaration_article_key"]
        logger.debug("Параметры переноса: %s", config_data)

        registry_wb = load_workbook(
            path.normpath(config_data["paths"]["registry_path"]))
        logger.info("Открыт реестр: %s", config_data["paths"]["registry_path"])
        declaration_wb = load_workbook(
            path.normpath(config_data["paths"]["declaration_path"]))
        logger.info("Открыта декларация: %s", config_data["paths"]["declaration_path"])

        registry_sheet = registry_wb.active
        declaration_sheet = declaration_wb.active

        registry_articles = dict()
        for registry_row in range(int(config_data["start_rows"]["registry_start_row"]), registry_sheet.max_row + 1):
            registry_article_cell = self._normalize_article(
                registry_sheet[registry_article_key + str(registry_row)].value)
            if registry_article_cell:
                registry_articles[registry_article_cell] = registry_row
        logger.info("Найдено артикулов в реестре: %s", len(registry_articles))

        matched_rows = 0
        copied_cells = 0
        for declaration_row in range(int(config_data["start_rows"]["declaration_start_row"]), declaration_sheet.max_row + 1):
            declaration_article_cell = self._normalize_article(
                declaration_sheet[declaration_article_key + str(declaration_row)].value)
            if declaration_article_cell in registry_articles:
                matched_rows += 1
                registry_row = registry_articles[declaration_article_cell]
                for registry_sign in config_data["transfer_pairs"].keys():
                    declaration_sheet[config_data["transfer_pairs"][registry_sign] + str(
                        declaration_row)] = registry_sheet[registry_sign + str(registry_row)].value
                    copied_cells += 1
        logger.info("Совпавших строк: %s, перенесено ячеек: %s", matched_rows, copied_cells)

        registry_wb.close()
        declaration_wb.save(path.normpath(self.path_to_temp_declaration))
        declaration_wb.close()
        logger.info("Временная декларация сохранена: %s", self.path_to_temp_declaration)

    def open_temp_declaration(self) -> None:
        logger.info("Открытие временной декларации: %s", self.path_to_temp_declaration)
        Utility.start_file(self.path_to_temp_declaration)

    def save_temp_declaration(self, save_path: str) -> None:
        logger.info("Сохранение декларации: %s", save_path)
        file = load_workbook(
            path.normpath(self.path_to_temp_declaration))
        file.save(path.normpath(save_path))
        file.close()
        logger.info("Декларация сохранена: %s", save_path)

    def delete_temp_declaration(self) -> None:
        if not path.exists(path.normpath(self.path_to_temp_declaration)):
            return

        logger.debug("Удаление временной декларации: %s", self.path_to_temp_declaration)
        remove(path.normpath(self.path_to_temp_declaration))
