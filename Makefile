.PHONY: build


build:
	nuitka --standalone --onefile --windows-icon-from-ico=assets/icon.ico --output-filename=DataTransferApp --include-data-files=app_info.json=app_info.json --windows-console-mode=disable --lto=yes main.py