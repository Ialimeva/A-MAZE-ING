class Config:
    def __init__(self) -> None:
        self.__width: int = 20
        self.__height: int = 15
        self.__entry: tuple[int, int] = (0, 0)
        self.__exit: tuple[int, int] = (19, 14)
        self.__output_file: str = "maze.txt"
        self.__perfect: bool = True

    def get_config(self) -> dict[
        str,
        int | tuple[int, int] | str | bool
    ]:
        config: dict[
            str,
            int | tuple[int, int] | str | bool
        ] = {}

        config["width"] = self.__width
        config["height"] = self.__height
        config["entry"] = self.__entry
        config["exit"] = self.__exit
        config["output_file"] = self.__output_file
        config["perfect"] = self.__perfect

        return config

    def set_width(self, width: int) -> None:
        self.__width = width

    def set_height(self, height: int) -> None:
        self.__height = height

    def set_entry(self, entry: tuple[int, int]) -> None:
        self.__entry = entry

    def set_exit(self, exit: tuple[int, int]) -> None:
        self.__exit = exit

    def set_output_file(self, output_file: str) -> None:
        self.__output_file = output_file

    def set_perfect(self, perfect: bool) -> None:
        self.__perfect = perfect


# TODO: Implement class / function to validate configuration,
# and stick to default one if error happen

class ConfigManager:
    def __init__(self, filename: str) -> None:
        if not filename:
            raise ValueError("No configuration file provided")
        self._filename: str = filename

