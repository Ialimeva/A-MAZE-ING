"""Provide utilities for exporting mazes to files.

This module contains functionality for writing maze data and
solution paths to disk.
"""

from typing import Optional


class MazeWriterError(Exception):
    """Raise when a maze cannot be written to a file."""

    pass


class MazeWriter:
    """Write mazes and their solutions to files."""

    @classmethod
    def write_maze(
        cls,
        filename: str,
        grid_hex: list[list[str]],
        entry_point: Optional[tuple[int, int]],
        exit_point: Optional[tuple[int, int]],
        path: Optional[list[tuple[int, int]]] = None,
        is_cell: bool = False
    ) -> None:
        """Write a maze and its metadata to a file.

        The output file contains the maze representation followed
        optionally by the entry point, exit point, and solution path.

        Args:
            filename: Destination file.
            grid_hex: Maze represented as hexadecimal values.
            entry_point: Entry point of the maze.
            exit_point: Exit point of the maze.
            path: Optional solution path.
            is_cell: Optional indication of the grid format.

        Raises:
            MazeWriterError: If the output file is invalid or the
                export operation fails.
        """
        try:
            if not filename:
                raise MazeWriterError("Invalid file")
            with open(filename, "w") as f:
                output: str = "\n".join("".join(row) for row in grid_hex)
                f.write(output)
                f.write("\n")

                if (entry_point and exit_point):
                    f.write("\n")
                    f.write(
                        str(entry_point[0]) +
                        "," +
                        str(entry_point[1]) + "\n"
                    )
                    f.write(
                        str(exit_point[0]) +
                        "," +
                        str(exit_point[1]) + "\n"
                    )

                if path:
                    output = MazeWriter.__parse_path(path, is_cell)
                    f.write(output + "\n")

        except Exception as e:
            raise MazeWriterError(f"Export failed: {e}")

    @staticmethod
    def __parse_path(path: list[tuple[int, int]], is_cell: bool) -> str:
        """Convert a solution path into cardinal directions.

        Consecutive positions are translated into a string
        containing the directions ``N``, ``E``, ``S``, and ``W``.

        Args:
            path: Sequence of positions describing the solution.
            is_cell: Optional indication of the grid format.

        Returns:
            The solution path encoded as a direction string.
        """
        step: int = 2 if is_cell else 1
        directions: dict[tuple[int, int], str] = {
            (0, -step): "N",
            (step, 0): "E",
            (0, step): "S",
            (-step, 0): "W",
        }

        res: str = ""
        for i in range(len(path) - 1):
            x = path[i + 1][0] - path[i][0]
            y = path[i + 1][1] - path[i][1]
            res += directions[(x, y)]

        return res
