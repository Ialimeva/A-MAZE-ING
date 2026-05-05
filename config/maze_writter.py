from typing import Optional


class MazeWritterError(Exception):
    pass


class MazeWritter:

    @classmethod
    def write_maze(
        cls,
        filename: str,
        grid_hex: list[list[str]],
        entry_point: Optional[tuple[int, int]],
        exit_point: Optional[tuple[int, int]],
        path: Optional[str] = None
    ) -> None:
        try:
            if not filename:
                raise MazeWritterError("Invalid file")
            with open(filename, "w") as f:
                output: str = "\n".join("".join(row) for row in grid_hex)
                f.write(output)
                f.write("\n")

                if (entry_point and exit_point):
                    f.write("\n")
                    f.write(str(entry_point[0]) + "," + str(entry_point[1]) + "\n")
                    f.write(str(exit_point[0]) + "," + str(exit_point[1]) + "\n")

                if path:
                    f.write("\n")
                    f.write(path + "\n")

        except Exception as e:
            raise MazeWritterError(f"Export failed: {e}")
