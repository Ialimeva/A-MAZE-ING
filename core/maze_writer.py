from typing import Optional


class MazeWriterError(Exception):
    pass


class MazeWriter:

    @classmethod
    def write_maze(
        cls,
        filename: str,
        grid_hex: list[list[str]],
        entry_point: Optional[tuple[int, int]],
        exit_point: Optional[tuple[int, int]],
        path: Optional[list[tuple[int, int]]] = None
    ) -> None:
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
                    output = MazeWriter.__parse_path(path)
                    f.write(output + "\n")

        except Exception as e:
            raise MazeWriterError(f"Export failed: {e}")

    @staticmethod
    def __parse_path(path: list[tuple[int, int]]) -> str:
        directions: dict[tuple[int, int], str] = {
            (0, -2): "N",
            (2, 0): "E",
            (0, 2): "S",
            (-2, 0): "W",
        }

        res: str = ""
        for i in range(len(path) - 1):
            x = path[i + 1][0] - path[i][0]
            y = path[i + 1][1] - path[i][1]
            res += directions[(x, y)]

        return res
