from abc import ABC, abstractmethod
from typing import Generator
import random


class SolverError(Exception):
    pass


class MazeSolver(ABC):
    def __init__(
        self,
        grid: list[list[int]],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        seed: int
    ) -> None:
        if not grid or len(grid) < 2:
            raise SolverError(f"Invalid grid")
        if (
            grid[entry_point[1]][entry_point[0]] == 2 or
            grid[exit_point[1]][exit_point[0]] == 2
        ):
            raise SolverError("Given coordinate collide with untouchable wall in the maze")

        self._grid: list[list[int]] = grid
        self._entry: tuple[int, int] = entry_point
        self._exit: tuple[int, int] = exit_point
        self._random: random.Random = random.Random(seed)

    @abstractmethod
    def solve(self) -> str:
        ...

    @abstractmethod
    def solve_step(self) -> Generator:
        ...

    def is_valid_pos(self, x: int, y: int) -> bool:
        width: int = len(self._grid[0])
        height: int = len(self._grid)

        return (
            0 < x < width and 
            0 < y < height and 
            self._grid[y][x] != 2
        )
