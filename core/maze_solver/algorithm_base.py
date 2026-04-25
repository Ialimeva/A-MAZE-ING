from abc import ABC, abstractmethod
from typing import Generator


class SolverError(Exception):
    pass


class MazeSolver(ABC):
    def __init__(
        self,
        grid: list[list[int]]
    ) -> None:
        if not grid or len(grid) < 2:
            raise SolverError(f"Invalid grid")
        self._grid: list[list[int]] = grid

    @abstractmethod
    def solve(self) -> None:
        ...

    @abstractmethod
    def solve_step(self) -> Generator:
        ...
