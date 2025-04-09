from flet import app
from src.ui.ui_script import UIScript
from updater import Updater
from sys import argv


if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == "--no_update":
            app(UIScript)
    else:
        updater = Updater()
        update_triggered = updater.run_updater(argv[0])
        if not update_triggered:
            app(UIScript)