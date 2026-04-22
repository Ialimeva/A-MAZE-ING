from abc import ABC, abstractmethod

class MazeAlgoError(Exception):
    pass

class MazeAlgorithm(ABC):
    def __init__(
        self,
        width: int,
        height: int,
        grid: list[list[int]]
    ) -> None:
        self.__width: int = width
        self.__height: int = height
        self._grid: list[list[int]] = grid

    @abstractmethod
    def generate(self) -> list[list[int]]:
        ...

    # TODO: Generate maze but one step at a time
    # @abstractmethod
    # def generate_step(self) -> list[list[int]]:
    #     ...

    def is_valid_pos(self, x: int, y: int) -> bool:
        return (
            0 < x < self.__width and
            0 < y < self.__height and
            self._grid[y][x] != 2
        )
