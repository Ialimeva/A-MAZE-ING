"""
    Contain simple call of the mazegen package
"""

from mazegen import Maze
from mazegen.maze_config import MazeConfig
from .generator import MazeGenerator
from .solver import MazeSolver
from typing import Optional, Generator


class MazeGen:
    """
        Represent MazeGen, a simple utilization of the mazegen package
    """
    @staticmethod
    def initiate_grid(width: int, height: int) -> list[list[int]]:
        """
            Initialization of the grid

            Args:
                width, height (int): Size of the grid

            Return:
                list[list[int]]: the grid initialized
        """
        return MazeGenerator.initiate_grid(width, height)

    @staticmethod
    def generate(
        generator_cls: type[MazeGenerator],
        config: MazeConfig,
    ) -> Maze:
        """
            Generate the maze at once

            Args:
                generator_cls (typle[MazeGenerator]): instance of MazeGenerator
                config (MazeConfig): configuration use for the algorithm

            Return:
                Maze: The full maze generate
        """
        generator: MazeGenerator = generator_cls(config)
        return generator.generate()

    @staticmethod
    def generate_step(
        generator_cls: type[MazeGenerator],
        config: MazeConfig,
    ) -> Generator[Maze, None, None]:
        """
            Generate the maze step by step

            Args:
                generator_cls (typle[MazeGenerator]): instance of MazeGenerator
                config (MazeConfig): configuration use for the algorithm

            Return:
                yield position carve
                Maze: The full maze
        """
        generator: MazeGenerator = generator_cls(config)
        yield from generator.generate_step()

    @staticmethod
    def solve(
        solver_cls: type[MazeSolver],
        maze: Maze,
        seed: Optional[int] = None
    ) -> list[tuple[int, int]]:
        """
            Solve the maze at once

            Args:
                solver_cls (typle[MazeGenerator]): instance oSolver
                maze (Maze): The maze to solve
                seed (Optional[int]): for the random choice

            Return:
                Maze: The full maze generate
        """
        solver: MazeSolver = solver_cls(maze, seed)
        return solver.solve()

    @staticmethod
    def solve_step(
        solver_cls: type[MazeSolver],
        maze: Maze,
        seed: Optional[int] = None
    ) -> Generator[tuple[int, int], None, list[tuple[int, int]]]:
        """
            Solve the maze at step by step

            Args:
                solver_cls (typle[MazeGenerator]): instance oSolver
                maze (Maze): The maze to solve
                seed (Optional[int]): for the random choice

            Return:
                yield position visited
                Maze: The full maze generate
        """
        solver: MazeSolver = solver_cls(maze, seed)
        return (yield from solver.solve_step())
