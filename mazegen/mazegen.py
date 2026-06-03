"""Simple interface for maze generation and solving."""

from mazegen import Maze
from mazegen.maze_config import MazeConfig
from .generator import MazeGenerator
from .solver import MazeSolver
from typing import Optional, Generator


class MazeGen:
    """Interface for maze generation and solving operations."""

    @staticmethod
    def initiate_grid(width: int, height: int) -> list[list[int]]:
        """Initialize a solid maze grid.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.

        Returns:
            2D grid initialized with wall values.
        """
        return MazeGenerator.initiate_grid(width, height)

    @staticmethod
    def generate(
        generator_cls: type[MazeGenerator],
        config: MazeConfig,
    ) -> Maze:
        """Generate a complete maze.

        Args:
            generator_cls: Generator algorithm class.
            config: Maze configuration.

        Returns:
            Generated Maze instance.
        """
        generator: MazeGenerator = generator_cls(config)
        return generator.generate()

    @staticmethod
    def generate_step(
        generator_cls: type[MazeGenerator],
        config: MazeConfig,
    ) -> Generator[Maze, None, None]:
        """Generate a maze incrementally.

        Args:
            generator_cls: Generator algorithm class.
            config: Maze configuration.

        Yields:
            Intermediate maze states during generation.
        """
        generator: MazeGenerator = generator_cls(config)
        yield from generator.generate_step()

    @staticmethod
    def solve(
        solver_cls: type[MazeSolver],
        maze: Maze,
        seed: Optional[int] = None
    ) -> list[tuple[int, int]]:
        """Solve a maze completely.

        Args:
            solver_cls: Solver algorithm class.
            maze: Maze to solve.
            seed: Random seed for reproducibility.

        Returns:
            Solution path as list of coordinates.
        """
        solver: MazeSolver = solver_cls(maze, seed)
        return solver.solve()

    @staticmethod
    def solve_step(
        solver_cls: type[MazeSolver],
        maze: Maze,
        seed: Optional[int] = None
    ) -> Generator[tuple[int, int], None, list[tuple[int, int]]]:
        """Solve a maze incrementally.

        Args:
            solver_cls: Solver algorithm class.
            maze: Maze to solve.
            seed: Random seed for reproducibility.

        Yields:
            Visited coordinates during solving.
        """
        solver: MazeSolver = solver_cls(maze, seed)
        return (yield from solver.solve_step())
