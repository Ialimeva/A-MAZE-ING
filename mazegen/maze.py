"""
    Maze format, handle all maze property: width, height, grid, grid_hex,
    entry and exit point.

    Handle (2x + 1) format in list[list[int]] and
    hexadecimal format in LSB condition format
"""

from typing import Optional


class MazeError(Exception):
    """
        Error raised by the maze
    """
    pass


# TODO: : Merge contract Maze to Cell Representation instead of a full
#       list[list[int]] (heavy space), Optimization version
class Maze:
    """
        Represent the maze itself and expose its property

        Attributes:
            width (int): number of columns in the maze grid
            height (int): number of row in the maze grid
            entry, exit (tuple[int, int]): position of the entry and exit point
            grid: list[list[int]]: 2D grid of the maze
    """
    def __init__(
        self,
        grid: Optional[list[list[int]]] = None,
        entry_point: Optional[tuple[int, int]] = None,
        exit_point: Optional[tuple[int, int]] = None
    ) -> None:
        """
            Constructor of class Maze, initialization of attribut

            Args:
                grid (Optional[list[list[int]]]): Default to None
                entry_point (Optional[tuple[int, int]]): Default to None,
                    position of the entry point
                exit_point (Optional[tuple[int, int]]): Default to None,
                    position of the exit point
        """
        self.__grid: list[list[int]] = grid or []
        self.__entry: Optional[tuple[int, int]] = entry_point
        self.__exit: Optional[tuple[int, int]] = exit_point

        if entry_point:
            self.__entry = entry_point
        if exit_point:
            self.__exit = exit_point

    @property
    def width(self) -> int:
        """
            Width of the grid (2x + 1 format)

            Return:
                int: width
        """
        return (len(self.__grid[0]) if self.__grid else 0)

    @property
    def height(self) -> int:
        """
            Height of the grid (2x + 1 format)

            Return:
                int: height
        """
        return (len(self.__grid) if self.__grid else 0)

    @property
    def grid(self) -> list[list[int]]:
        """
            Grid (2x + 1 format)

            Return:
                list[list[int]]: grid
        """
        return self.__grid

    @property
    def grid_hex(self) -> list[list[str]]:
        """
            Grid (hexadecimal format)

            Return:
                list[list[int]]: grid
        """
        return self.__parsing_hex()

    @property
    def entry(self) -> tuple[int, int]:
        """
            Entry Point position in the Maze

            Return:
                tuple[int, int]: position of the point

            Raise:
                MazeError: on empty position
        """
        if self.__entry is None:
            raise MazeError("No Entry point given")
        return (2 * self.__entry[0] + 1, 2 * self.__entry[1] + 1)

    @property
    def exit(self) -> tuple[int, int]:
        """
            Exit Point position in the Maze

            Return:
                tuple[int, int]: position of the point

            Raise:
                MazeError: on empty position
        """
        if self.__exit is None:
            raise MazeError("No Exit point given")
        return (2 * self.__exit[0] + 1, 2 * self.__exit[1] + 1)

    def __parsing_hex(self) -> list[list[str]]:
        """
            Parser of the grid (2x + 1) format to hexadecimal format

            Return:
                list[list[str]]: the hexadecimal format
                of the attribut self.__grid

            Raise:
                MazeError: on invalid, empty self.__grid
        """

        if not self.__grid:
            raise MazeError("Empty grid")
        output: list[list[str]] = []
        height: int = len(self.__grid)
        width: int = len(self.__grid[0])

        for i in range(1, height - 1, 2):
            row: list[str] = []
            for j in range(1, width - 1, 2):
                west = self.__grid[i][j - 1]
                south = self.__grid[i + 1][j]
                east = self.__grid[i][j + 1]
                north = self.__grid[i - 1][j]

                value = (
                    (north << 0) |
                    (east << 1) |
                    (south << 2) |
                    (west << 3)
                )

                row += [format(value, "X")]
            output += [row]

        return output

    def set_grid(self, grid: list[list[int]]) -> None:
        """
            Setter grid

            Args:
                grid (list[list[int]])
        """
        self.__grid = grid

    def set_entry(self, entry_point: tuple[int, int]) -> None:
        """
            Setter entry point

            Args:
                entry_point (tuple[int, int])
        """
        self.__entry = entry_point

    def set_exit(self, exit_point: tuple[int, int]) -> None:
        """
            Setter exit point

            Args:
                exit_point (tuple[int, int])
        """
        self.__exit = exit_point

    def set_path(self, x: int, y: int) -> None:
        """
            Setter path, carve wall, etc

            Args:
                x (int), y (int): Position of the point on the grid
        """
        try:
            self.grid[y][x] = 0
        except Exception as e:
            raise MazeError(e)

    def get_value(self, x: int, y: int) -> int:
        """
            Getter value of position on the grid

            Args:
                x (int), y (int): Position needed

            Return:
                int: Value of the positon on the grid
        """
        try:
            return self.grid[y][x]
        except Exception as e:
            raise MazeError(e)
