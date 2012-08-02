ENV_DIR = ./var
ACTIVATE_ENV = . $(ENV_DIR)/bin/activate;
REQUIREMENT = ./requirements.txt

create_env:
	@echo "=> Creating a virtual environment."
	mkdir $(ENV_DIR)
	virtualenv $(ENV_DIR)

create_cfg:
	@echo "=> Creating configuration file in current environment."
	touch $(ENV_DIR)/config.cfg
	echo 'export SIGMAGO_CONFIG="$$VIRTUAL_ENV/config.cfg"' >> $(ENV_DIR)/bin/activate

install_libs: $(REQUIREMENT)
	@echo "=> Installing required libraries from PyPI."
	$(ACTIVATE_ENV) pip install -r $(REQUIREMENT)

init_env: create_env create_cfg install_libs
	@echo "=> Initializing current virtual environment."

destory_env: $(ENV_DIR)
	@echo "=> Removing the virtual enviroment."
	rm -rf $(ENV_DIR)
	@echo "=> Please enter next command to leave virtual environment."
	@echo "deactivate"

env: $(ENV_DIR)
	@echo "=> Please enter next command to enter virtual enviroment."
	@echo $(ACTIVATE_ENV)
