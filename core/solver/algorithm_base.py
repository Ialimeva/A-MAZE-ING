from abc import ABC, abstractmethod
from typing import Generator
import random

from core.maze import Maze

class SolverError(Exception):
    pass


class MazeSolver(ABC):
    def __init__(
        self,
        maze: Maze,
        seed: int
    ) -> None:
        self._maze: Maze = maze
        self._random: random.Random = random.Random(seed)

    @abstractmethod
    def solve(self) -> str:
        ...

    @abstractmethod
    def solve_step(self) -> Generator:
        ...

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (
            0 < x < self._maze.width and
            0 < y < self._maze.height and
            self._maze.grid[y][x] != 2
        )
