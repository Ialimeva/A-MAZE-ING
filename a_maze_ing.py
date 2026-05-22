#!/usr/bin/env python3

import sys
from typing import Any
from core import ConfigManager
from mazegen import GeneratorRegistry, SolverRegistry, Maze
from cli_render import VisualTerm
from display import Game, DisplayConfig


def usage_exit() -> None:
    print("No argument or multiple arguments found")
    print("Usage: \033[34mpython a_maze_ing.py <file config>\033[0m")
    print("Please try again :)")
    sys.exit(1)


def get_config(filename: str) -> dict[str, Any]:
    return ConfigManager(
        filename,
        GeneratorRegistry.avaliable(),
        SolverRegistry.avaliable()
    ).get_config()


def main() -> None:
    if len(sys.argv) != 2:
        usage_exit()

    configs: dict[str, Any] = get_config(sys.argv[1])
    print(configs)
    print("\033[H\033[J")
    if configs["visual"] == "term":
        term_render: VisualTerm = VisualTerm(configs)
        term_render.run()
    else:
        print("Need Meva")


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(f"Caught exception: {e}")

    except (KeyboardInterrupt, EOFError):
        print()
        print("=== Program Stopped ===")
        print()
