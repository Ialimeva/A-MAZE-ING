from ..algorithm_base import MazeAlgoError, MazeAlgorithm
from typing import Generator, Optional


class Backtracking(MazeAlgorithm):
    def __init__(
        self,
        width: int,
        height: int,
        grid: Optional[list[list[int]]] | None = None,
        perfect: bool = True,
        seed: Optional[int] = None
    ) -> None:
        super().__init__(width, height, grid, perfect, seed)
        self.__visited: set[tuple[int, int]] = set()

    def generate(self) -> list[list[int]]:
        self.__visited.clear()
        if not self.__carve(1, 1):
            raise MazeAlgoError("Error on generating the Maze")
        return super().generate()

    def __carve(
        self,
        start_x: int,
        start_y: int
    ) -> bool:
        self.__visited.clear()

        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.__visited.add((start_x, start_y))
        self._grid[start_y][start_x] = 0

        while stack:
            pos_x, pos_y = stack[-1]

            directions: list[tuple[int, int]] = [
                (2, 0),
                (-2, 0),
                (0, -2),
                (0, 2)
            ]
            self._random.shuffle(directions)

            pushed: bool = False
            for dx, dy in directions:
                npos_x, npos_y = dx + pos_x, dy + pos_y

                if (
                    self.is_valid_pos(npos_x, npos_y) and
                    (npos_x, npos_y) not in self.__visited
                ):
                    self.__visited.add((npos_x, npos_y))
                    stack.append((npos_x, npos_y))

                    self._grid[(dy // 2) + pos_y][(dx // 2) + pos_x] = 0
                    self._grid[npos_y][npos_x] = 0

                    pushed = True
                    break

            if not pushed:
                stack.pop()

        return True

    def generate_step(self) -> Generator[list[list[int]], None, None]:
        self.__visited.clear()

        yield self._grid
        yield from self.__carve_step(1, 1)
        yield from super().generate_step()

    def __carve_step(
        self,
        start_x: int,
        start_y: int
    ) -> Generator[list[list[int]], None, None]:
        self.__visited.clear()

        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.__visited.add((start_x, start_y))
        self._grid[start_y][start_x] = 0

        while stack:
            pos_x, pos_y = stack[-1]

            directions: list[tuple[int, int]] = [
                (2, 0),
                (-2, 0),
                (0, -2),
                (0, 2)
            ]
            self._random.shuffle(directions)

            pushed: bool = False
            for dx, dy in directions:
                npos_x, npos_y = dx + pos_x, dy + pos_y

                if (
                    self.is_valid_pos(npos_x, npos_y) and
                    (npos_x, npos_y) not in self.__visited
                ):
                    self.__visited.add((npos_x, npos_y))
                    stack.append((npos_x, npos_y))

                    self._grid[(dy // 2) + pos_y][(dx // 2) + pos_x] = 0
                    self._grid[npos_y][npos_x] = 0

                    yield self._grid

                    pushed = True
                    break

            if not pushed:
                stack.pop()

        yield self._grid
