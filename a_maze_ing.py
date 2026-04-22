#!/usr/bin/env python3

import sys
from core import ConfigManager


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Invalid execution format - try:\n"
            "python3 a_maze_ing.py <config_file>"
        )
        sys.exit(1)

    try:
        config: ConfigManager = ConfigManager(sys.argv[1])

        all_configuration: dict[
            str,
            str | bool | int | tuple[int, int]
        ] = config.get_config()

        print(all_configuration)
    except ValueError as e:
        print(f"Value error: {e}")


if __name__ == "__main__":
    print("=== A-Maze-ing ===\n")
    main()
