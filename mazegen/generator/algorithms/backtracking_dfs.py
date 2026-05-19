from ..generator_base import MazeGenerator
from typing import Generator
from mazegen.maze import Maze
from mazegen.maze_config import MazeConfig


class GeneratorDFS(MazeGenerator):
    algorithm_name = "dfs"

    def __init__(
        self,
        configs: MazeConfig,
    ) -> None:
        super().__init__(configs)
        self.__visited: set[tuple[int, int]] = set()

    def __carve(
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

    def generate(self) -> Maze:
        self.__visited.clear()
        gen = self.__carve(1, 1)

        for val in gen:
            self._maze = val
        return super().generate()

    def generate_step(self) -> Generator[Maze, None, None]:
        self.__visited.clear()
        gen = self.__carve(1, 1)

        yield self._maze
        yield from gen
        yield from super().generate_step()
