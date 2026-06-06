"""Provide utilities for creating, solving, and exporting mazes.

This module centralizes access to maze generators, solvers, and
file export functionality.
"""

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
    """Provide utility methods for maze generation, solving, and exporting."""

    @staticmethod
    def initiate_maze(
        maze: Maze,
        width: int,
        height: int
    ) -> None:
        """Initialize a maze with an empty grid.

        Args:
            maze: Maze instance to initialize.
            width: Width of the maze in cells.
            height: Height of the maze in cells.
        """
        grid: list[list[int]] = MazeGenerator.initiate_grid(width, height)
        maze.set_grid(grid)

    @staticmethod
    def get_generator(name: str) -> type:
        """Retrieve a maze generator class.

        If the requested generator is ``"auto"``, the default DFS
        generator is returned.

        Args:
            name: Name of the generator.

        Returns:
            The generator class associated with the given name.
        """
        return (
            GeneratorRegistry.get("dfs") if name.lower() == "auto"
            else GeneratorRegistry.get(name)
        )

    @staticmethod
    def get_solver(name: str) -> type:
        """Retrieve a maze solver class.

        If the requested solver is ``"auto"``, the default BFS
        solver is returned.

        Args:
            name: Name of the solver.

        Returns:
            The solver class associated with the given name.
        """
        return (
            SolverRegistry.get("bfs") if name.lower() == "auto"
            else SolverRegistry.get(name)
        )

    @staticmethod
    def generate(configs: dict[str, Any]) -> Maze:
        """Generate a maze from the provided configuration.

        Args:
            configs: Configuration dictionary.

        Returns:
            The generated maze.
        """
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
        """Generate a maze incrementally.

        Args:
            configs: Configuration dictionary.

        Yields:
            Intermediate states of the maze during generation.
        """
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
    def solve(
        maze: Maze,
        configs: dict[str, Any]
    ) -> list[tuple[int, int]]:
        """Solve a maze.

        Args:
            maze: Maze to solve.
            configs: Configuration dictionary.

        Returns:
            The path from the entry point to the exit point.
        """
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
        """Solve a maze incrementally.

        Args:
            maze: Maze to solve.
            configs: Configuration dictionary.

        Yields:
            Coordinates visited during the solving process.

        Returns:
            The complete solution path.
        """
        gen = MazeGen.solve_step(
            solver_cls=MazeManager.get_solver(configs["solver"]),
            maze=maze,
            seed=configs["seed"]
        )
        return (yield from gen)

    @staticmethod
    def grid_to_cell(pos: tuple[int, int]) -> tuple[int, int]:
        """Convert grid coordinates into cell coordinates.

        Args:
            pos: Position in the grid.

        Returns:
            The corresponding cell coordinates.
        """
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
        path: Optional[list[tuple[int, int]]] = None,
        is_cell: Optional[bool] = False
    ) -> None:
        """Write a maze to a file.

        Args:
            filename: Destination file.
            grid_hex: Maze represented as hexadecimal values.
            entry_point: Entry point of the maze.
            exit_point: Exit point of the maze.
            path: Optional solution path to include in the output.
            is_cell: Optional indication of the grid format.
        """
        MazeWriter.write_maze(
            filename,
            grid_hex,
            entry_point,
            exit_point,
            path,
            is_cell or False
        )
