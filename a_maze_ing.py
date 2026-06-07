#!/usr/bin/env python3

"""Entry point for the A-Maze-ing application.

This module handles command-line execution, configuration loading,
and selection of the visualization mode (terminal or graphical).

It coordinates:
    - configuration parsing via ConfigManager
    - maze generation and solving registries
    - rendering selection (terminal or game mode)
"""

import sys
from typing import Any
from core import ConfigManager
from mazegen import GeneratorRegistry, SolverRegistry
from cli_render import VisualTerm
from display import Game
import time


def usage_exit() -> None:
    """Print usage instruction and exit with the value 1 status."""
    print("No argument or multiple arguments found")
    print("Usage: \033[34mpython a_maze_ing.py <file config>\033[0m")
    print("Please try again :)")
    sys.exit(1)


def introduction() -> None:
    """Display the A-Maze-ing ASCII banner with a loading animation."""
    a_maze_ing: str = r"""
 █████╗       ███╗   ███╗ █████╗ ███████╗███████╗      ██╗███╗   ██╗ ██████╗
██╔══██╗      ████╗ ████║██╔══██╗╚══███╔╝██╔════╝      ██║████╗  ██║██╔════╝
███████║█████╗██╔████╔██║███████║  ███╔╝ █████╗  █████╗██║██╔██╗ ██║██║  ███╗
██╔══██║╚════╝██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ╚════╝██║██║╚██╗██║██║   ██║
██║  ██║      ██║ ╚═╝ ██║██║  ██║███████╗███████╗      ██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝╚═╝  ╚═══╝ ╚═════╝
    """
    print("\033[H\033[J")
    output: list[str] = str(a_maze_ing).split("\n")
    for line in output:
        print(line)
        time.sleep(0.1)


def get_config(filename: str) -> dict[str, Any]:
    """Load and validate the configuration from a file.

    Args:
        filename: Path to the configuration file.

    Returns:
        The configuration as a dictionary of key-value pairs.
    """
    return ConfigManager(
        filename,
        GeneratorRegistry.available(),
        SolverRegistry.available()
    ).get_config()


def print_config(configs: dict[str, Any]) -> None:
    """Display the configuration used for the current execution.

    Args:
        configs: Configuration dictionary containing the program settings.
    """
    output: str = "\n=== Configuration ===\n"

    output += "WIDTH: " + f"{configs['width']}\n"
    output += "HEIGHT: " + f"{configs['height']}\n"
    output += "ENTRY: " + f"{configs['entry']}\n"
    output += "EXIT: " + f"{configs['exit']}\n"
    output += "OUTPUT FILE: " + f"{configs['output_file']}\n"
    output += "PERFECT: " + f"{configs['perfect']}\n"
    output += "SEED: " + f"{configs['seed']}\n"
    output += "GENERATOR: " + f"{configs['generator']}\n"
    output += "SOLVER: " + f"{configs['solver']}\n"
    output += "VISUAL: " + f"{configs['visual']}\n"
    output += "STORY: " + f"{configs['story']}\n"
    output += "=====================\n"

    print(output)


def main() -> None:
    """Run the A-Maze-ing program.

    Validate the command-line arguments, display the introduction,
    load the configuration file, and start the selected visualization.

    Available configuration keys are:
        - width
        - height
        - entry
        - exit
        - output_file
        - perfect
        - seed
        - generator
        - solver
        - visual
        - story
    """
    if len(sys.argv) != 2:
        usage_exit()

    introduction()

    configs: dict[str, Any] = get_config(sys.argv[1])
    print_config(configs)

    if configs["story"]:
        pass

    if configs["visual"] == "term":
        term_render: VisualTerm = VisualTerm(configs)
        term_render.run()
    else:
        game = Game(configs)
        game.run()


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(f"Caught exception: {e}")

    except (KeyboardInterrupt, EOFError):
        print()
        print("=== Program Stopped ===")
        print()
