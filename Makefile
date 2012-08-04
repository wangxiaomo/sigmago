ENV_DIR = ./var
ACTIVATE_ENV = . $(ENV_DIR)/bin/activate;
REQUIREMENT = ./requirements.txt

create_env:
	@echo "=> Creating a virtual environment." >&2
	mkdir -p $(ENV_DIR)
	virtualenv $(ENV_DIR)

create_cfg:
	@echo "=> Creating configuration file in current environment." >&2
	touch $(ENV_DIR)/config.cfg
	echo 'export SIGMAGO_CONFIG="$$VIRTUAL_ENV/config.cfg"' >> $(ENV_DIR)/bin/activate

install_libs: $(REQUIREMENT)
	@echo "=> Installing required libraries from PyPI." >&2
	$(ACTIVATE_ENV) pip install -r $(REQUIREMENT)

init_env: create_env create_cfg install_libs
	@echo "=> Initializing current virtual environment." >&2

destory_env: $(ENV_DIR)
	@echo "=> Removing the virtual enviroment." >&2
	rm -rf $(ENV_DIR)
	@echo "=> Please enter next command to leave virtual environment." >&2
	@echo "deactivate"

env: $(ENV_DIR)
	@echo "=> Please enter next command to enter virtual enviroment." >&2
	@echo $(ACTIVATE_ENV)
