from typing import Any, Generator, Optional
from mazegen import MazeGenerator
from .forty_two_pattern import Pattern42
from mazegen import (
    Maze,
    MazeConfig,
    MazeGen,
    GeneratorRegistry,
    SolverRegistry
)
from .maze_writer import MazeWriter


class MazeManager:
    @staticmethod
    def initiate_maze(
        maze: Maze,
        width: int,
        height: int
    ) -> None:
        grid: list[list[int]] = MazeGenerator.initiate_grid(width, height)
        maze.set_grid(grid)

    @staticmethod
    def get_generator(name: str) -> type:
        return (
            GeneratorRegistry.get("dfs") if name.lower() == "auto"
            else GeneratorRegistry.get(name)
        )

    @staticmethod
    def get_solver(name: str) -> type:
        return (
            SolverRegistry.get("bfs") if name.lower() == "auto"
            else SolverRegistry.get(name)
        )

    @staticmethod
    def generate(configs: dict[str, Any]) -> Maze:
        grid, _ = Pattern42.create_grid_42pattern(
            configs["width"],
            configs["height"]
        )
        maze_conf: MazeConfig = MazeConfig(
            width=configs["width"],
            height=configs["height"],
            entry_point=configs["entry"],
            exit_point=configs["exit"],
            perfect=configs["perfect"],
            seed=configs["seed"],
            grid=grid
        )

        return (
            MazeGen.generate(
                config=maze_conf,
                generator_cls=MazeManager.get_generator(configs["generator"]),
            )
        )

    @staticmethod
    def generate_step(configs: dict[str, Any]) -> Generator[Maze, None, None]:
        grid, _ = Pattern42.create_grid_42pattern(
            configs["width"],
            configs["height"]
        )
        maze_conf: MazeConfig = MazeConfig(
            width=configs["width"],
            height=configs["height"],
            entry_point=configs["entry"],
            exit_point=configs["exit"],
            perfect=configs["perfect"],
            seed=configs["seed"],
            grid=grid
        )

        yield from (
            MazeGen.generate_step(
                config=maze_conf,
                generator_cls=MazeManager.get_generator(configs["generator"]),
            )
        )

    @staticmethod
    def solve(maze: Maze, configs: dict[str, Any]) -> list[tuple[int, int]]:
        return (
            MazeGen.solve(
                solver_cls=MazeManager.get_solver(configs["solver"]),
                maze=maze,
                seed=configs["seed"]
            )
        )

    @staticmethod
    def solve_step(
        maze: Maze,
        configs: dict[str, Any]
    ) -> Generator[tuple[int, int], None, list[tuple[int, int]]]:
        gen = MazeGen.solve_step(
            solver_cls=MazeManager.get_solver(configs["solver"]),
            maze=maze,
            seed=configs["seed"]
        )
        return (yield from gen)

    @staticmethod
    def grid_to_cell(pos: tuple[int, int]) -> tuple[int, int]:
        x: int = 0
        y: int = 0
        try:
            x, y = pos[0] // 2, pos[1] // 2
        except Exception as e:
            print(f"[Grid to Cell value] Can't export ({x}, {y}): {e}")
        return (x, y)

    @staticmethod
    def write_maze(
        filename: str,
        grid_hex: list[list[str]],
        entry_point: Optional[tuple[int, int]],
        exit_point: Optional[tuple[int, int]],
        path: Optional[list[tuple[int, int]]] = None
    ) -> None:
        MazeWriter.write_maze(
            filename,
            grid_hex,
            entry_point,
            exit_point, path
        )
