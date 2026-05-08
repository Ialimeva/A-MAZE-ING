from mazegen import Maze
from mazegen.maze_config import MazeConfig
from .generator import MazeGenerator
from .solver import MazeSolver
from typing import Optional, Generator


class MazeGen:
    @staticmethod
    def generate(
        generator_cls: type[MazeGenerator],
        config: MazeConfig,
        grid: Optional[list[list[int]]] = None
    ) -> Maze:
        generator: MazeGenerator = generator_cls(config, grid)
        return generator.generate()

    @staticmethod
    def generate_step(
        generator_cls: type[MazeGenerator],
        config: MazeConfig,
        grid: Optional[list[list[int]]] = None
    ) -> Generator[Maze, None, None]:
        generator: MazeGenerator = generator_cls(config, grid)
        yield from generator.generate_step()


    @staticmethod
    def solve(
        solver_cls: type[MazeSolver],
        maze: Maze,
        seed: Optional[int] = None
    ) -> list[tuple[int, int]]:
        solver: MazeSolver = solver_cls(maze, seed)
        return solver.solve()

    @staticmethod
    def solve_step(
        solver_cls: type[MazeSolver],
        maze: Maze,
        seed: Optional[int] = None
    ) -> Generator[list[tuple[int, int]], None, None]:
        solver: MazeSolver = solver_cls(maze, seed)
        yield from solver.solve_step()
