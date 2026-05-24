from dataclasses import dataclass
from typing import Any, Generator
from mazegen import MazeGenerator
from .forty_two_pattern import Pattern42
from mazegen import (
    Maze,
    MazeConfig,
    MazeGen,
    GeneratorRegistry,
    SolverRegistry
)


@dataclass
class SolverFrame:
    visited: tuple[int, int] | None
    solution: list[tuple[int, int]] | None


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
    ) -> Generator[SolverFrame, None, None]:
        gen = MazeGen.solve_step(
            solver_cls=MazeManager.get_solver(configs["solver"]),
            maze=maze,
            seed=configs["seed"]
        )

        try:
            while True:
                pos = next(gen)
                yield SolverFrame(
                    visited=pos,
                    solution=None
                )
        except StopIteration as e:
            yield SolverFrame(
                visited=None,
                solution=e.value
            )

    @staticmethod
    def grid_to_cell(pos: tuple[int, int]) -> tuple[int, int]:
        x: int = 0
        y: int = 0
        try:
            x, y = pos[0] // 2, pos[1] // 2
        except Exception as e:
            print(f"[Grid to Cell value] Can't export ({x}, {y}): {e}")
        return (x, y)
