# Installation
PYTHON_INSTALL = python3

# Environment Configuration
VENV		= .venv
PYTHON		= $(VENV)/bin/python
PIP			= $(PYTHON) -m pip

RM = rm -rf

# Creating the package -> .whl/ .tar
build: $(VENV)
	@ echo "> Building mazegen package"
	@ $(PYTHON) -m build --outdir .
	@ $(RM) $(VENV)

$(VENV)		:
	@ echo "> Building environment"
	@ $(PYTHON_INSTALL) -m venv $@
	@ $(PIP) install build --quiet
