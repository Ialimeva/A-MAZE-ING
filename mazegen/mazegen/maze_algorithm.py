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

    def is_position_outbound(self, x: int, y: int) -> bool:
        if (x < 0 or x > self.__width):
            return False
        if (y < 0 or y > self.__height):
            return False
        if (self._grid[x][y] == 2):
            return False
        return True

