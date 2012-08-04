ENV_DIR = ./var
ENV_ACTIVATE = $(ENV_DIR)/bin/activate
ACTIVATE = . $(ENV_ACTIVATE);
REQUIREMENT = ./requirements.txt
PIP_CACHE_DIR = $(ENV_DIR)/.pip_download_cache
CONFIG_FILENAME = config.cfg

create_env:
	@echo "=> Creating a virtual environment." >&2
	mkdir -p $(ENV_DIR)
	virtualenv --no-site-package $(ENV_DIR)

create_cfg:
	@echo "=> Creating configuration file in current environment." >&2
	touch $(ENV_DIR)/config.cfg

install_libs: $(REQUIREMENT)
	@echo "=> Installing required libraries." >&2
	$(ACTIVATE) pip install --download-cache $(PIP_CACHE_DIR) \
		-r $(REQUIREMENT)

init_env: create_env create_cfg
	@echo "=> Initializing current virtual environment." >&2
	mkdir -p $(ENV_DIR)/$(PIP_CACHE_DIRNAME)
	echo 'export SIGMAGO_CONFIG="$$VIRTUAL_ENV/$(CONFIG_FILENAME)"' \
		>> $(ENV_ACTIVATE)

init: init_env install_libs

destory_env: $(ENV_DIR)
	@echo "=> Removing the virtual enviroment." >&2
	rm -rf $(ENV_DIR)
	@echo "=> Please enter next command to leave virtual environment." >&2
	@echo "deactivate"

env: $(ENV_DIR)
	@echo "=> Please enter next command to enter virtual enviroment." >&2
	@echo $(ACTIVATE)

check:
	@echo "=> Checking the coding style."
	pep8 ./sigmago
	pep8 ./tests
	pyflakes ./sigmago
	pyflakes ./tests
