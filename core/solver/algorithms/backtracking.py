from core.solver.algorithm_base import MazeSolver, SolverError
from typing import Generator, Optional
from core.maze import Maze


class Backtracking(MazeSolver):
    def __init__(self, maze: Maze, seed: Optional[int] = None) -> None:
        super().__init__(maze, seed)
        self.__visited: set[tuple[int, int]] = set()
        self.__path: list[tuple[int, int]] = []

    def solve(self) -> list[tuple[int, int]]:
        if not self.__find():
            raise solvererror("error on solving the maze")
        return (self.__path)

    def __find(self) -> bool:
        self.__visited.clear()

        stack: list[tuple[int, int]] = [self._maze.entry]
        self.__path = [self._maze.entry]
        self.__visited.add(self._maze.entry)

        while stack:
            pos_x, pos_y = stack[-1]

            directions: list[tuple[int, int]] = [
                (0, -2),
                (2, 0),
                (0, 2),
                (-2, 0)
            ]
            self._random.shuffle(directions)

            pushed: bool = False
            for dx, dy in directions:
                npos_x, npos_y = dx + pos_x, dy + pos_y
                if (
                    self.is_valid_pos(npos_x, npos_y) and
                    (npos_x, npos_y) not in self.__visited
                ):
                    if (npos_x, npos_y) == self._maze.exit:
                        self.__path += [(npos_x, npos_y)]
                        return True

                    if (self._maze.grid[(dy // 2) + pos_y][(dx // 2) + pos_x] == 0):
                        self.__visited.add((npos_x, npos_y))
                        stack += [(npos_x, npos_y)]
                        self.__path += [(npos_x, npos_y)]
                        pushed = True
                        break

            if not pushed:
                stack.pop()
                self.__path.pop()

        return False

    def solve_step(self) -> Generator[list[tuple[int, int]], None, None]:
        yield from self.__find_step()
        yield self.__path

    def __find_step(self) -> Generator[list[tuple[int, int]], None, None]:
        self.__visited.clear()

        stack: list[tuple[int, int]] = [self._maze.entry]
        self.__path = [self._maze.entry]
        self.__visited.add(self._maze.entry)

        while stack:
            pos_x, pos_y = stack[-1]

            directions: list[tuple[int, int]] = [
                (0, -2),
                (2, 0),
                (0, 2),
                (-2, 0)
            ]
            self._random.shuffle(directions)

            pushed: bool = False
            for dx, dy in directions:
                npos_x, npos_y = dx + pos_x, dy + pos_y
                if (
                    self.is_valid_pos(npos_x, npos_y) and
                    (npos_x, npos_y) not in self.__visited
                ):
                    if (npos_x, npos_y) == self._maze.exit:
                        self.__path += [(npos_x, npos_y)]
                        yield self.__path
                        return

                    if (self._maze.grid[(dy // 2) + pos_y][(dx // 2) + pos_x] == 0):
                        self.__visited.add((npos_x, npos_y))
                        stack += [(npos_x, npos_y)]
                        self.__path += [(npos_x, npos_y)]

                        yield self.__path
                        pushed = True

                        if (npos_x, npos_y) == self._maze.exit:
                            self.__path += [(npos_x, npos_y)]
                            yield self.__path
                            return
                        break

            if not pushed:
                stack.pop()
                self.__path.pop()

        yield self.__path
