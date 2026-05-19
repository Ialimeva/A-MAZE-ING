#!/usr/bin/env python3

import sys
from typing import Any
from config import MazeManager, ConfigManager, MazeWriter
from mazegen import Maze, GeneratorRegistry, SolverRegistry
from cli_render import Render
from display import Game, DisplayConfig

def usage_and_exit() -> None:
    print("Usage: python/python3 a_maze_ing.py <config file>")
    print("Try again please !!")
    sys.exit(1)


def get_config(filename: str) -> dict[str, Any]:
    return ConfigManager(
        filename,
        GeneratorRegistry.avaliable(),
        SolverRegistry.avaliable()
    ).get_config()


def main() -> None:
    if len(sys.argv) != 2:
        usage_and_exit()

    configs: dict[str, Any] = get_config(sys.argv[1])
    maze: Maze = Maze()
    path: list[tuple[int, int]] = []
    render: Render = Render()

    # gen = MazeManager.generate_step(configs)
    # for g in gen:
    #     maze = g
    #     render.render_maze(maze)

    # gen = MazeManager.solve_step(maze, configs)
    # visited: list[tuple[int, int]] = []
    # for sf in gen:
    #     if sf.visited is not None:
    #         visited.append(sf.visited)

    #     if sf.solution is not None:
    #         path = sf.solution

    #     render.render_maze(maze=maze, path=visited)

    # render.render_maze(maze=maze, path=render._expand_path(path))

    #Display(MEVA)
    display_config: DisplayConfig = DisplayConfig(
        columns = configs["width"],
        rows = configs["height"]
    )
    MazeManager.initiate_maze(maze, configs["width"], configs["height"])
    maze = MazeManager.generate(configs)
    game = Game(display_config, maze, configs)
    game.run()
    MazeWriter.write_maze(
        configs["output_file"],
        maze.grid_hex,
        configs["entry"],
        configs["exit"],
        path
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Caught error: {e}")
    except KeyboardInterrupt:
        print("\n=== Program Stoped ===\n")
