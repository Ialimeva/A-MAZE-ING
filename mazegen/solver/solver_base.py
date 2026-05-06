from abc import ABC, abstractmethod
from typing import Generator, Optional
import random
from mazegen.maze import Maze


class SolverError(Exception):
    pass


class MazeSolver(ABC):
    def __init__(
        self,
        maze: Maze,
        seed: Optional[int] = None
    ) -> None:
        self._maze: Maze = maze
        self._random: random.Random = random.Random(seed)

    @abstractmethod
    def solve(self) -> list[tuple[int, int]]:
        ...

    @abstractmethod
    def solve_step(self) -> Generator[list[tuple[int, int]], None, None]:
        ...

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (
            0 < x < self._maze.width and
            0 < y < self._maze.height and
            self._maze.grid[y][x] not in (1, 2)
        )
