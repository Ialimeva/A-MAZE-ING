from ..generator_base import GeneratorError, MazeGenerator
from typing import Generator, Optional
from mazegen.maze import Maze
from mazegen.maze_config import MazeConfig


class GeneratorDFS(MazeGenerator):
    def __init__(
        self,
        configs: MazeConfig,
        grid: Optional[list[list[int]]] = None
    ) -> None:
        super().__init__(configs, grid)
        self.__visited: set[tuple[int, int]] = set()

    def generate(self) -> Maze:
        self.__visited.clear()
        if not self.__carve(1, 1):
            raise GeneratorError("Error on generating the Maze")
        return super().generate()

    def __carve(
        self,
        start_x: int,
        start_y: int
    ) -> bool:
        self.__visited.clear()

        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.__visited.add((start_x, start_y))
        self._maze.grid[start_y][start_x] = 0

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

                    self._maze.grid[(dy // 2) + pos_y][(dx // 2) + pos_x] = 0
                    self._maze.grid[npos_y][npos_x] = 0

                    pushed = True
                    break

            if not pushed:
                stack.pop()

        return True

    def generate_step(self) -> Generator[Maze, None, None]:
        self.__visited.clear()

        yield self._maze
        yield from self.__carve_step(1, 1)
        yield from super().generate_step()

    def __carve_step(
        self,
        start_x: int,
        start_y: int
    ) -> Generator[Maze, None, None]:
        self.__visited.clear()

        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.__visited.add((start_x, start_y))
        self._maze.grid[start_y][start_x] = 0

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

                    self._maze.grid[(dy // 2) + pos_y][(dx // 2) + pos_x] = 0
                    self._maze.grid[npos_y][npos_x] = 0

                    yield self._maze

                    pushed = True
                    break

            if not pushed:
                stack.pop()

        yield self._maze
