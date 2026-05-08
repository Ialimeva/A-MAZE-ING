#!/usr/bin/env python3

import sys
from typing import Any, Optional
from config import ConfigManager, Pattern42, MazeWriter
from mazegen import Maze, MazeGenerator, GeneratorDFS, SolverBFS
from cli_render import Render


def usage_and_exit() -> None:
    print("Usage: python/python3 a_maze_ing.py <config file>")
    print("Try again please !!")
    sys.exit(1)


def get_config(filename: str) -> dict[str, Any]:
    return ConfigManager(filename).get_config()


def algo_generator(
    algo: str,
    width: int, height: int,
    entry_point: tuple[int, int], exit_point: tuple[int, int],
    seed: Optional[int],
    grid: Optional[list[list[int]]],
    perfect: bool = True
) -> MazeGenerator:
    if algo.lower() == "dfs":
        return GeneratorDFS(
            width,
            height,
            entry_point,
            exit_point,
            seed=seed,
            grid=grid,
            perfect=perfect
        )
    return GeneratorDFS(
        width,
        height,
        entry_point,
        exit_point,
        seed=seed,
        grid=grid,
        perfect=perfect
    )


def main() -> None:
    if len(sys.argv) != 2:
        usage_and_exit()

    configs: dict[str, Any] = get_config(sys.argv[1])
    grid, _ = Pattern42.create_grid_42pattern(
        configs["width"],
        configs["height"]
    )

    generator: MazeGenerator = algo_generator(
        "DFS",
        width=configs["width"],
        height=configs["height"],
        entry_point=configs["entry"],
        exit_point=configs["exit"],
        seed=configs["seed"],
        grid=grid,
        perfect=configs["perfect"]
    )
    render: Render = Render()

    gen = generator.generate_step()
    maze: Maze = Maze()
    for g in gen:
        maze = g
        render.render_maze(maze)

    solver: SolverBFS = SolverBFS(maze)
    path: list[tuple[int, int]] = []
    gen = solver.solve_step()

    for g in gen:
        path = g
        render.render_maze(maze, path)
    full_path = render._expand_path(path)
    render.render_maze(maze, full_path)

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
