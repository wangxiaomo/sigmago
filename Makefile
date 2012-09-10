ENV_DIR = ./var
ENV_ACTIVATE = $(ENV_DIR)/bin/activate
ACTIVATE = . $(ENV_ACTIVATE);
REQUIREMENT = ./requirements.txt
PIP_CACHE_DIR = $(ENV_DIR)/.pip_download_cache
CONFIG_FILENAME = config.cfg
GIT_PRE_COMMIT = "./.git/hooks/pre-commit"

create_env:
	@echo "=> Creating a virtual environment." >&2
	mkdir -p $(ENV_DIR)
	virtualenv --no-site-package $(ENV_DIR)
	echo "sigmago-dev" > $(ENV_DIR)/__name__

create_cfg:
	@echo "=> Creating configuration file in current environment." >&2
	touch $(ENV_DIR)/config.cfg

install_libs: $(REQUIREMENT)
	@echo "=> Installing required libraries." >&2
	$(ACTIVATE) pip install --download-cache $(PIP_CACHE_DIR) \
		-r $(REQUIREMENT)
	@echo "=> Initializing Git Submodules." >&2
	git submodule init
	@echo "=> Creating links of this project in site-packages directory." >&2
	python setup.py develop

init_env: create_env create_cfg
	@echo "=> Initializing current virtual environment." >&2
	mkdir -p $(ENV_DIR)/$(PIP_CACHE_DIRNAME)
	echo 'export SIGMAGO_CONFIG="$$VIRTUAL_ENV/$(CONFIG_FILENAME)"' \
		>> $(ENV_ACTIVATE)

install_githook:
	@echo "=> Installing git hooks to check source before commit."
	cp ./misc/githooks/pre-commit $(GIT_PRE_COMMIT)
	chmod +x $(GIT_PRE_COMMIT)

install_node: misc/install-node
	$(ACTIVATE) misc/install-node

init: init_env install_libs install_githook

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
	$(ACTIVATE) pep8 ./sigmago
	$(ACTIVATE) pep8 ./tests
	$(ACTIVATE) pyflakes ./sigmago
	$(ACTIVATE) pyflakes ./tests

test:
	$(ACTIVATE) python setup.py test

clean:
	find . -name "*.log" -type f | xargs rm -f
	find . -name "*.pyc" -type f | xargs rm -f
	find . -name "*.pyo" -type f | xargs rm -f
	find ./sigmago/static -name "*.min.js" -type f | xargs rm -f
	find ./sigmago/static -name "*.min.css" -type f | xargs rm -f
