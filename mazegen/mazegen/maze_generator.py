from .maze_algorithm import MazeAlgorithm
from typing import Optional


class MazeError(Exception):
    pass

class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        grid: Optional[list[list[int]]] = None,
        algo: Optional[MazeAlgorithm] = None,
    ) -> None:
        if width < 0:
            raise MazeError(f"Invalid width: {width}")
        self.__width: int = (2 * width) + 1

        if height < 0:
            raise MazeError(f"Invalid height: {height}")
        self.__height: int = (2 * height) + 1

        self.__grid: list[list[int]] = []
        if grid:
            self.__grid = grid
        else:
            self.__grid = MazeGenerator.initiate_grid(
                self.__width,
                self.__height
            )

        self.__algo: MazeAlgorithm
        if algo:
            self.__algo = algo

    def set_algo(self, algo: MazeAlgorithm):
        self.__algo = algo

    @staticmethod
    def initiate_grid(width: int, height: int) -> list[list[int]]:
        return [
            [1 for _ in range(width)]
            for _ in range(height)
        ]

    def generate(self) -> list[list[int]]:
        return self.__algo.generate()
