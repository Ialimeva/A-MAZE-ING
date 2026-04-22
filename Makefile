# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trakotoz <trakotoz@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/21 17:45:13 by trakotoz          #+#    #+#              #
#    Updated: 2026/04/22 09:07:00 by trakotoz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# Environment Configuration
VENV		= .venv
PYTHON		= $(VENV)/bin/python
PIP			= $(PYTHON) -m pip
REQ			= requirements.txt

# Program and Args
PROGRAM		= a_maze_ing.py
CONFIG		= config.txt

RM	= rm -rf

# Color
C_RESET		= \033[0m
C_GREEN		= \033[032m
C_YELLOW	= \033[33m
C_BLEU		= \033[34m
C_MAGENTA	= \033[35m


$(VENV)	:
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


install		: $(VENV)
	@ echo "$(C_MAGENTA)> Installing $(REQ)$(C_RESET)"
	@ $(PIP) install -r $(REQ)

run			: install
	$(PYTHON) $(PROGRAM) $(CONFIG)

clean		:
	@ echo "$(C_YELLOW)Removing python cache$(C_RESET)"
	@ $(RM) $(shell find . -name "__pycache__" -type d)

	@ echo "$(C_YELLOW)Removing other cache$(C_RESET)"
	@ $(RM) $(shell find . -name ".mypy_cache" -type d)

fclean		: clean
	@ echo "$(C_YELLOW)Removing virtual environment$(C_RESET)"
	@ $(RM) $(VENV)

lint 		: install
	@ $(PYTHON) -m flake8 --exclude=$(VENV)
	@ $(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict	: install
	@ $(PYTHON) -m flake8 --exclude=$(VENV)
	@ $(PYTHON) -m mypy . --strict

# TODO: Implemetation of command to run the program in debug mode
debug		: run

.PHONY	: install run clean lint lint-strict
