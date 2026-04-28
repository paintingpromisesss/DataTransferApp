from flet.app import app
from logging import getLogger
from src.config_system.logging_service import LoggingService
from src.config_system.utility import Utility
from src.ui.ui_script import UIScript
import traceback


if __name__ == "__main__":
    LoggingService.setup_logging()
    logger = getLogger(__name__)
    try:
        logger.info("Запуск приложения")
        app(UIScript, assets_dir=Utility.get_assets_directory())
    except Exception:
        logger.exception("Приложение завершилось с непредвиденной ошибкой")
        traceback.print_exc()
        input("\nНажмите Enter, чтобы закрыть программу...")
        raise
