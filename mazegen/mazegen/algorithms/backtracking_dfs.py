from ..algorithm_base import MazeAlgoError, MazeAlgorithm
import random
from typing import Generator

class Backtracking(MazeAlgorithm):
    def __init__(
        self,
        width: int,
        height: int,
        grid: list[list[int]]
    ) -> None:
        super().__init__(width, height, grid)
        self.__visited: set[tuple[int, int]] = set()

    def generate(self) -> list[list[int]]:
        self.__visited.clear()
        if not self.__carve(1, 1):
            raise MazeAlgoError("Error on generating the Maze")
        return self._grid

    def __carve(
        self,
        pos_x: int,
        pos_y: int
    ) -> bool:
        self._grid[pos_y][pos_x] = 0
        self.__visited.add((pos_x, pos_y))

        directions: list[tuple[int, int]] = [
            (2, 0),
            (-2, 0),
            (0, 2),
            (0, -2)
        ]
        random.shuffle(directions)

        for dx, dy in directions:
            npos_x, npos_y = pos_x + dx, pos_y + dy

            if self.is_valid_pos(npos_x, npos_y) and (npos_x, npos_y) not in self.__visited:
                self._grid[(dy // 2) + pos_y][(dx // 2) + pos_x] = 0
                self.__carve(npos_x, npos_y)

        return True

    def generate_step(self) -> Generator[list[list[int]], None, None]:
        self.__visited.clear()

        yield self._grid
        yield from self.__carve_step(1, 1)
        yield self._grid

    def __carve_step(self, pos_x: int, pos_y: int) -> Generator[list[list[int]], None, None]:
        self._grid[pos_y][pos_x] = 0
        self.__visited.add((pos_x, pos_y))

        directions: list[tuple[int, int]] = [
            (2, 0),
            (-2, 0),
            (0, 2),
            (0, -2)
        ]
        random.shuffle(directions)

        for dx, dy in directions:
            npos_x, npos_y = pos_x + dx, pos_y + dy
            if (self.is_valid_pos(npos_x, npos_y) and (npos_x, npos_y) not in self.__visited):
                self._grid[(dy // 2) + pos_y][(dx // 2) + pos_x] = 0
                yield self._grid
                yield from self.__carve_step(npos_x, npos_y)

        yield self._grid
