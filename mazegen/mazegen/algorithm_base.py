from abc import ABC, abstractmethod
from typing import Generator, Optional
import random


class MazeAlgoError(Exception):
    pass


class MazeAlgorithm(ABC):
    def __init__(
        self,
        width: int,
        height: int,
        grid: Optional[list[list[int]]] | None = None,
        perfect: bool = True,
        seed: Optional[int] = None
    ) -> None:
        self.__width: int = width
        self.__height: int = height
        self._grid: list[list[int]] = (
            grid if grid is not None
            else MazeAlgorithm.initiate_grid(self.__width, self.__height)
        )

        self._perfect: bool = perfect

        self._random: random.Random = random.Random(seed)

    @abstractmethod
    def generate(self) -> list[list[int]]:
        ...

    @abstractmethod
    def generate_step(self) -> Generator[list[list[int]], None, None]:
        ...

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (
            0 < x < self.__width and
            0 < y < self.__height and
            self._grid[y][x] != 2
        )

    @staticmethod
    def initiate_grid(width: int, height: int) -> list[list[int]]:
        return [
            [1 for _ in range(width)]
            for _ in range(height)
        ]

    @classmethod
    def _add_loop(cls, grid: list[list[int]]) -> list[list[int]]:
        return grid
