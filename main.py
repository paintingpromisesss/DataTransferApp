from flet.app import app
from src.config_system.utility import Utility
from src.ui.ui_script import UIScript
import traceback


if __name__ == "__main__":
    try:
        app(UIScript, assets_dir=Utility.get_assets_directory())
    except Exception:
        traceback.print_exc()
        input("\nНажмите Enter, чтобы закрыть программу...")
        raise