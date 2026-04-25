from abc import ABC, abstractmethod
from typing import Generator, Optional
import random


class MazeAlgoError(Exception):
    pass


class MazeAlgorithm(ABC):
    _chance: float = 0.1

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
        if not self._perfect:
            self._add_loop()
        return self._grid

    @abstractmethod
    def generate_step(self) -> Generator[list[list[int]], None, None]:
        if not self._perfect:
            self._add_loop()
        yield self._grid

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

    def _add_loop(self) -> None:
        import time

        print("Adding loops")
        time.sleep(2)
        for y in range(1, self.__height - 1):
            for x in range(1, self.__width - 1):
                if self._grid[y][x] == 2:
                    continue
                if self._grid[y][x] != 1:
                    continue

                neighbors: int = 0
                if self._grid[y - 1][x] == 0:
                    neighbors += 1
                if self._grid[y][x + 1] == 0:
                    neighbors += 1
                if self._grid[y + 1][x] == 0:
                    neighbors += 1
                if self._grid[y][x - 1] == 0:
                    neighbors += 1

                if neighbors >= 2 and self._random.random() < MazeAlgorithm._chance:
                    self._grid[y][x] = 0

        print("Adding loops finished")
