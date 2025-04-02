from flet import app
from src.ui.ui_script import UIScript
from sys import exit, argv, executable
from subprocess import Popen
from os import path
import updater
if __name__ == "__main__":
    updater = updater.Updater()
    if len(argv) > 1 and argv[1] == "--update-mode":
        download_url = argv[2]
        updater.run_update(download_url)
        exit()

    download_url = updater.check_for_updates()
    if download_url:
        print("Update available. Downloading...")
        current_executable = path.abspath(argv[0])
        Popen([executable, "--update-mode", download_url])
        exit()
    else:
        print("No updates available. Starting application...")
        app(UIScript)