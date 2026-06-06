"""Base class for maze solving algorithms."""

from abc import ABC, abstractmethod
from typing import Generator, Optional
import random
from ..maze import Maze
from ..maze_register import SolverRegistry


class SolverError(Exception):
    """Error raised by solver operations."""

    pass


class MazeSolver(ABC):
    """Base class for maze-solving algorithms."""

    algorithm_name: str | None = None

    def __init__(
        self,
        maze: Maze,
        seed: Optional[int] = None
    ) -> None:
        """Initialize the maze solver.

        Args:
            maze: Maze to solve.
            seed: Random seed for reproducibility.
        """
        self._maze: Maze = maze
        self._random: random.Random = random.Random(seed)

    def __init_subclass__(cls) -> None:
        """Automatically register solver subclasses in the solver registry.

        When a subclass defines an ``algorithm_name``, it is automatically
        registered into the :class:`SolverRegistry`.

        This enables dynamic discovery of all available solver implementations.

        Args:
            cls: The subclass being initialized.
        """
        super().__init_subclass__()

        if cls.algorithm_name is not None:
            SolverRegistry.register(
                cls.algorithm_name,
                cls
            )

    @abstractmethod
    def solve(self) -> list[tuple[int, int]]:
        """Find a path from start to goal.

        Returns:
            List of coordinates forming the solution path.
        """
        ...

    @abstractmethod
    def solve_step(self) -> Generator[
        tuple[int, int],
        None,
        list[tuple[int, int]]
    ]:
        """Find a path incrementally.

        Yields:
            Visited coordinates during solving.
        """
        ...

    def is_valid_pos(self, x: int, y: int) -> bool:
        """Check if a position is valid and traversable.

        Args:
            x: X-coordinate.
            y: Y-coordinate.

        Returns:
            True if valid, False otherwise.
        """
        return (
            0 < x < self._maze.width and
            0 < y < self._maze.height and
            self._maze.get_value(x, y) not in (1, 2)
        )
