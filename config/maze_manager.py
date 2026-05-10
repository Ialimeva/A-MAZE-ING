from dataclasses import dataclass
from mazegen import (
    Maze,
    MazeConfig,
    MazeGen,
    GeneratorRegistry,
    SolverRegistry
)
from typing import Any, Generator
from .forty_two_pattern import Pattern42


@dataclass
class SolverFrame:
    visited: tuple[int, int] | None
    solution: list[tuple[int, int]] | None


class MazeManager:
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
