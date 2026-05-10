from abc import ABC, abstractmethod
from typing import Generator, Optional
import random
from mazegen.maze import Maze
from mazegen.maze_register import SolverRegistry


class SolverError(Exception):
    pass


class MazeSolver(ABC):

    algorithm_name: str | None = None

    def __init__(
        self,
        maze: Maze,
        seed: Optional[int] = None
    ) -> None:
        self._maze: Maze = maze
        self._random: random.Random = random.Random(seed)

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.algorithm_name is not None:
            SolverRegistry.register(
                cls.algorithm_name,
                cls
            )

    @abstractmethod
    def solve(self) -> list[tuple[int, int]]:
        ...

    @abstractmethod
    def solve_step(self) -> Generator[tuple[int, int], None, list[tuple[int, int]]]:
        ...

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (
            0 < x < self._maze.width and
            0 < y < self._maze.height and
            self._maze.grid[y][x] not in (1, 2)
        )
