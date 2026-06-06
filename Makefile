# Installation
PYTHON_INSTALL = python3

# Environment Configuration
VENV		= .venv
PYTHON		= $(VENV)/bin/python
FLAKE8		= $(PYTHON) -m flake8
MYPY		= $(PYTHON) -m mypy

PIP			= $(PYTHON) -m pip
REQ			= requirements.txt

# Program and Args
PROGRAM		= a_maze_ing.py
CONFIG		= config.txt

RM			= rm -rf

# Color
C_RESET		= \033[0m
C_GREEN		= \033[032m
C_YELLOW	= \033[33m
C_BLUE		= \033[34m
C_MAGENTA	= \033[35m

DIST		= dist $(shell find . -name "*.egg-info" -type d)

all			: install

check		:
	@ command -v $(PYTHON_INSTALL) > /dev/null 2>&1 || { \
		echo "$(C_YELLOW)Error: Python is not installed$(C_RESET)"; \
		exit 1; \
	}

install		: $(VENV) check
	@ echo "$(C_MAGENTA)> Installing $(REQ)$(C_RESET)"
	@ $(PIP) install -r $(REQ) -q

$(VENV)		:
	@ echo "$(C_MAGENTA)> Creating Virtual environment$(C_RESET)"
	@ $(PYTHON_INSTALL) -m venv $@
	@ echo "$(C_MAGENTA)> Upgrade pip, latest version$(C_RESET)"
	@ $(PIP) install --upgrade pip -q

	@ echo
	@ echo "$(C_BLUE)Python:$(C_RESET)"
	@ $(PYTHON) --version

	@ echo "$(C_BLUE)Pip:$(C_RESET)"
	@ $(PIP) --version

	@ echo "$(C_RESET)"

run			: install
	@ $(PYTHON) $(PROGRAM) $(CONFIG)

clean		:
	@ echo "$(C_YELLOW)Removing python cache$(C_RESET)"
	@ $(RM) $(shell find . -name "__pycache__" -type d)

	@ echo "$(C_YELLOW)Removing other cache$(C_RESET)"
	@ $(RM) $(shell find . -name ".mypy_cache" -type d)

fclean		: clean
	@ echo "$(C_YELLOW)Removing virtual environment$(C_RESET)"
	@ $(RM) $(VENV)
	@ echo "$(C_YELLOW)Removing dist build generated file$(C_RESET)"
	@ $(RM) $(DIST)

lint 		: install
	@ $(FLAKE8)  --exclude=$(VENV)
	@ $(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict	: install
	@ $(FLAKE8) --exclude=$(VENV)
	@ $(MYPY) . --strict

debug		:
	@ $(PYTHON) -m ipdb $(PROGRAM) $(CONFIG)

re			: fclean all

packages	: $(VENV)
	@ $(PYTHON) --version
	@ $(PIP) list

build		: install
	@ $(PYTHON) -m build

help:
	@ echo "$(C_BLUE)Usage: make [target] $(C_RESET)"
	@ echo "$(C_GREEN)make install$(C_RESET)        Install all the dependencies"
	@ echo "$(C_GREEN)make run$(C_RESET)            Run $(PROGRAM) with $(CONFIG) as argument"
	@ echo "$(C_GREEN)make check$(C_RESET)          Verify Python is installed"
	@ echo "$(C_GREEN)make lint$(C_RESET)           Run flake8 and mypy (standard version)"
	@ echo "$(C_GREEN)make lint-strict$(C_RESET)    Run flake8 and mypy (strict version)"
	@ echo "$(C_GREEN)make debug$(C_RESET)          Run $(PROGRAM) under ipdb debugger"
	@ echo "$(C_GREEN)make packages$(C_RESET)       Show list of packages installed pip list"
	@ echo "$(C_GREEN)make build$(C_RESET)          Build mazegen packages"
	@ echo "$(C_GREEN)make clean$(C_RESET)          Remove python and mypy cache"
	@ echo "$(C_GREEN)make fclean$(C_RESET)         clean + remove virtualenv/dist"
	@ echo "$(C_GREEN)make re$(C_RESET)             fclean + install (rebuild of the project)"

.PHONY	: all install check run clean fclean lint lint-strict debug re packages build help
