.PHONY: build build-onefile build-standalone installer clean-artifacts

PYTHON ?= .venv/Scripts/python.exe
INNO_COMPILER ?= iscc
STANDALONE_DIR := main.dist

NUITKA_COMMON := --standalone --msvc=latest --include-windows-runtime-dlls=yes \
	--windows-icon-from-ico=assets/icon.ico \
	--output-filename=DataTransferApp \
	--company-name=paintingpromisesss \
	--product-name=DataTransferApp \
	--file-version=1.1.0.0 \
	--product-version=1.1.0.0 \
	--include-data-files=app_info.json=app_info.json \
	--include-data-dir=assets=assets \
	--include-raw-dir=.venv/Lib/site-packages/flet_desktop/app/flet=flet_desktop/app/flet \
	--windows-console-mode=disable \
	--lto=no

build: build-onefile

build-onefile:
	$(PYTHON) -m nuitka $(NUITKA_COMMON) --onefile --onefile-no-compression --onefile-cache-mode=cached --onefile-tempdir-spec="{CACHE_DIR}/{COMPANY}/{PRODUCT}/{VERSION}" main.py

build-standalone:
	$(PYTHON) -m nuitka $(NUITKA_COMMON) main.py

installer: build-standalone
	$(INNO_COMPILER) installer/DataTransferApp.iss
	$(RM) -r $(STANDALONE_DIR)

clean-artifacts:
	$(RM) -r $(STANDALONE_DIR)
