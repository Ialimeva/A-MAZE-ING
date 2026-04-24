from ..algorithm_base import MazeSolver
from typing import Generator


class Backtracking(MazeSolver):
    def __init__(
        self,
        grid: list[list[int]]
    ) -> None:
        super().__init__(grid)

    def solve(self) -> None:
        ...

    def solve_step(self) -> Generator:
        ...
