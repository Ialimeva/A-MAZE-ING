from .algorithm_base import MazeAlgorithm
from .algorithms import Backtracking
from typing import Optional, Generator


class MazeError(Exception):
    pass


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        perfect: bool,
        grid: Optional[list[list[int]]] = None,
        algo: Optional[MazeAlgorithm] = None,
        seed: Optional[int] = None
    ) -> None:
        if width <= 0:
            raise MazeError(f"Invalid width: {width}")
        if height <= 0:
            raise MazeError(f"Invalid height: {height}")

        self.__width: int = (2 * width) + 1
        self.__height: int = (2 * height) + 1

        initial_grid: Optional[list[list[int]]] = (
            [row[:] for row in grid] if grid
            else None
        )
        self.__algo: MazeAlgorithm = (
            algo if algo
            else Backtracking(
                self.__width,
                self.__height,
                initial_grid,
                perfect,
                seed
            )
        )


    def set_algo(self, algo: MazeAlgorithm) -> None:
        self.__algo = algo


    def generate(self) -> list[list[int]]:
        return self.__algo.generate()

    def generate_step(self) -> Generator[list[list[int]], None, None]:
        return self.__algo.generate_step()
