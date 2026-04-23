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
        grid: list[list[int]],
        rdm: Optional[random.Random] = None
    ) -> None:
        self.__width: int = width
        self.__height: int = height
        self._grid: list[list[int]] = grid

        self._random: random.Random = random.Random()
        if rdm is not None:
            self._random = rdm

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
