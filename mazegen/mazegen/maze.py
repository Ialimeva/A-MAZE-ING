"""Maze representation with grid structure and solver path management."""

from typing import Optional


class MazeError(Exception):
    """Error raised by maze operations."""

    pass


class Maze:
    """Represents a maze grid with entry/exit points in (2x+1) format."""

    def __init__(
        self,
        grid: Optional[list[list[int]]] = None,
        entry_point: Optional[tuple[int, int]] = None,
        exit_point: Optional[tuple[int, int]] = None
    ) -> None:
        """Initialize a maze instance.

        Args:
            grid: 2D grid representing maze structure.
            entry_point: Entry coordinate as (x, y).
            exit_point: Exit coordinate as (x, y).
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
        """Return the number of columns in the maze grid."""
        return (len(self.__grid[0]) if self.__grid else 0)

    @property
    def height(self) -> int:
        """Return the number of rows in the maze grid."""
        return (len(self.__grid) if self.__grid else 0)

    @property
    def grid(self) -> list[list[int]]:
        """Return the raw integer grid representation."""
        return self.__grid

    @property
    def grid_hex(self) -> list[list[str]]:
        """Return the maze grid in hexadecimal format."""
        return self.__parsing_hex()

    @property
    def entry(self) -> tuple[int, int]:
        """Return the entry point coordinate.

        Raises:
            MazeError: If entry point is not set.
        """
        if self.__entry is None:
            raise MazeError("No Entry point given")
        return (2 * self.__entry[0] + 1, 2 * self.__entry[1] + 1)

    @property
    def exit(self) -> tuple[int, int]:
        """Return the exit point coordinate.

        Raises:
            MazeError: If exit point is not set.
        """
        if self.__exit is None:
            raise MazeError("No Exit point given")
        return (2 * self.__exit[0] + 1, 2 * self.__exit[1] + 1)

    def __parsing_hex(self) -> list[list[str]]:
        """Convert grid from (2x+1) format to hexadecimal format.

        Returns:
            2D list of hexadecimal values.

        Raises:
            MazeError: If grid is empty.
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
        """Replace the maze grid.

        Args:
            grid: 2D grid representing maze structure.
        """
        self.__grid = grid

    def set_entry(self, entry_point: tuple[int, int]) -> None:
        """Set the entry point.

        Args:
            entry_point: Coordinate as (x, y).
        """
        self.__entry = entry_point

    def set_exit(self, exit_point: tuple[int, int]) -> None:
        """Set the exit point.

        Args:
            exit_point: Coordinate as (x, y).
        """
        self.__exit = exit_point

    def set_path(self, x: int, y: int) -> None:
        """Mark a cell as a path (carve wall).

        Args:
            x: X-coordinate.
            y: Y-coordinate.

        Raises:
            MazeError: If coordinates are invalid.
        """
        try:
            self.grid[y][x] = 0
        except Exception as e:
            raise MazeError(e)

    def get_value(self, x: int, y: int) -> int:
        """Get the grid value at a coordinate.

        Args:
            x: X-coordinate.
            y: Y-coordinate.

        Returns:
            int: Grid value at the position.

        Raises:
            MazeError: If coordinates are invalid.
        """
        try:
            return self.grid[y][x]
        except Exception as e:
            raise MazeError(e)
