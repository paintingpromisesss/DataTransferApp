from logging import INFO, WARNING, Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler
from os import makedirs, path
from shutil import copy2

from src.config_system.utility import Utility

LOG_FILENAME = "DataTransferApp.log"
MAX_LOG_SIZE_BYTES = 300_000
BACKUP_LOG_COUNT = 2


class LoggingService:
    active_log_path = None

    @staticmethod
    def get_log_path() -> str:
        return path.join(Utility.get_program_directory(), LOG_FILENAME)

    @staticmethod
    def get_fallback_log_path() -> str:
        return path.join(Utility.get_config_directory(), LOG_FILENAME)

    @staticmethod
    def get_active_log_path() -> str:
        return LoggingService.active_log_path or LoggingService.get_log_path()

    @staticmethod
    def setup_logging() -> None:
        logger = getLogger()
        if logger.handlers:
            return

        formatter = Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        log_path = LoggingService.get_log_path()
        try:
            makedirs(path.dirname(log_path), exist_ok=True)
            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=MAX_LOG_SIZE_BYTES,
                backupCount=BACKUP_LOG_COUNT,
                encoding="utf-8"
            )
        except OSError:
            log_path = LoggingService.get_fallback_log_path()
            makedirs(path.dirname(log_path), exist_ok=True)
            file_handler = RotatingFileHandler(
                log_path,
                maxBytes=MAX_LOG_SIZE_BYTES,
                backupCount=BACKUP_LOG_COUNT,
                encoding="utf-8"
            )

        LoggingService.active_log_path = log_path
        file_handler.setFormatter(formatter)
        file_handler.setLevel(INFO)

        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(INFO)

        logger.setLevel(INFO)
        getLogger("flet").setLevel(WARNING)
        getLogger("flet_desktop").setLevel(WARNING)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.info("Логирование запущено. Файл логов: %s", log_path)

    @staticmethod
    def save_log_file(save_path: str) -> None:
        logger = getLogger(__name__)
        for handler in getLogger().handlers:
            handler.flush()

        copy2(LoggingService.get_active_log_path(), path.normpath(save_path))
        logger.info("Файл логов сохранен: %s", save_path)
