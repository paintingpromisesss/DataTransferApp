.PHONY: build


build:
	nuitka --standalone --onefile --windows-icon-from-ico=assets/icon.ico --windows-console-mode=disable --lto=yes main.py