from ..algorithm_base import MazeSolver
from typing import Generator


class Backtracking(MazeSolver):
    def __init__(
        self,
        grid: list[list[int]],
        entry_point: tuple[int, int],
        exit_point: tuple[int, int],
        seed: int
    ) -> None:
        super().__init__(grid, entry_point, exit_point, seed)
        self.__visited: set[tuple[int, int]] = set()

    def solve(self) -> str:
        self.__visited.clear()

        path: str = ""
        stack: list[tuple[int, int]] = [self._entry]
        self.__visited.add(self._entry)

        directions: list[tuple[int, int]] = [
            (2, 0),
            (-2, 0),
            (0, 2),
            (0, -2)
        ]

        while (stack):
            (x, y) = stack.pop()

            if (x, y) == self._exit:
                return path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                cx, cy = (dx // 2) + x, (dy // 2) + y

                if (
                    self.is_valid_pos(nx, ny) and
                    self._grid[cy][cx] == 0 and
                    (nx, ny) not in self.__visited
                ):
                    ...
                    self._random.choice()

        return path

    def solve_step(self) -> Generator:
        ...
