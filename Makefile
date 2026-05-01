
# Environment Configuration
VENV		= .venv
PYTHON		= $(VENV)/bin/python

PIP			= $(PYTHON) -m pip
REQ			= requirements.txt
DEP			= dependencies
MLX			= $(DEP)/mlx-2.2-py3-none-any.whl
NUMPY 		= numpy

# Program and Args
PROGRAM		= a_maze_ing.py
CONFIG		= config.conf

RM	= rm -rf

# Color
C_RESET		= \033[0m
C_GREEN		= \033[032m
C_YELLOW	= \033[33m
C_BLEU		= \033[34m
C_MAGENTA	= \033[35m

DIST	= dist $(shell find . -name "*.egg-info" -type d)

all		: install

install		: $(VENV)
	@ echo "$(C_MAGENTA)> Installing $(REQ)$(C_RESET)"
	@ $(PIP) install -r $(REQ) -q
	@ echo "$(C_MAGENTA)> Installing mlx $(C_RESET)"
	@ $(PIP) install $(MLX) -q
	@ $(PIP) install $(NUMPY) -q

$(VENV)		:
	@ echo "$(C_MAGENTA)> Creating Virtual environment$(C_RESET)"
	@ python3 -m venv $@
	@ echo "$(C_MAGENTA)> Upgrade pip, latest version$(C_RESET)"
	@ $(PIP) install --upgrade pip

	@ echo
	@ echo "$(C_BLEU)Python:$(C_RESET)"
	@ $(PYTHON) --version

	@ echo "$(C_BLEU)Pip:$(C_RESET)"
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
	@ $(PYTHON) -m flake8 --exclude=$(VENV)
	@ $(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict	: install
	@ $(PYTHON) -m flake8 --exclude=$(VENV)
	@ $(PYTHON) -m mypy . --strict

debug		: 
	@ $(PYTHON) -m ipdb $(PROGRAM)

re			: fclean all

packages	: install
	@ $(PIP) list
	@ $(PYTHON) --version
	@ $(PIP) --version

build		: install
	@ $(PYTHON) -m build

PHONY	: install run re clean lint lint-strict
