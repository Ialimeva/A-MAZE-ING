from typing import Optional
from .forty_two_pattern import Pattern42
from typing import Any


class ConfigError(Exception):
    pass


class Config:
    def __init__(self) -> None:
        self.__width: int = 20
        self.__height: int = 15
        self.__entry: tuple[int, int] = (0, 0)
        self.__exit: tuple[int, int] = (19, 14)
        self.__output_file: str = "maze.txt"
        self.__perfect: bool = True
        self.__seed: Optional[int] = None
        self.__generator: Optional[str] = "auto"
        self.__solver: Optional[str] = "auto"
        self.__visual: str = "mlx"

    def get_config(self) -> dict[str, Any]:
        config: dict[str, Any] = {}

        config["width"] = self.__width
        config["height"] = self.__height
        config["entry"] = self.__entry
        config["exit"] = self.__exit
        config["output_file"] = self.__output_file
        config["perfect"] = self.__perfect
        config["seed"] = self.__seed
        config["generator"] = self.__generator
        config["solver"] = self.__solver
        config["visual"] = self.__visual

        return config

    def set_width(self, width: int) -> None:
        if width <= 0:
            raise ConfigError(f"Invalid width value: {width}")
        self.__width = width

    def set_height(self, height: int) -> None:
        if height <= 0:
            raise ConfigError(f"Invalid height value {height}")
        self.__height = height

    def set_entry(self, entry: tuple[int, int]) -> None:
        if entry[0] < 0 or entry[1] < 0:
            raise ConfigError(f"Invalid entry point value {entry}")
        self.__entry = entry

    def set_exit(self, exit_: tuple[int, int]) -> None:
        if exit_[0] < 0 or exit_[1] < 0:
            raise ConfigError(f"Invalid exit point value {exit_}")
        self.__exit = exit_

    def set_output_file(self, output_file: str) -> None:
        if not output_file:
            raise ConfigError("Empty output_file")
        self.__output_file = output_file

    def set_perfect(self, perfect: bool) -> None:
        self.__perfect = perfect

    def set_seed(self, seed: str | Optional[int] = None) -> None:
        if not seed:
            return
        try:
            if str(seed).lower() == "none":
                self.__seed = None
                return

            val: int = int(seed)
            self.__seed = val
        except Exception:
            raise ConfigError(f"Invalid seed value {seed}")

    def set_generator(self, value: str) -> None:
        self.__generator = value.lower()

    def set_solver(self, value: str) -> None:
        self.__solver = value.lower()

    def set_visual(self, value: str) -> None:
        if not value:
            raise ConfigError(f"Invalid visual value {value}")
        if value.lower() == "mlx":
            self.__visual = "mlx"
        elif value.lower() == "term":
            self.__visual = "term"
        else:
            raise ConfigError(f"Invalid visual value {value}")


class ConfigManager:
    def __init__(
        self,
        filename: str,
        generators: dict[str, type],
        solvers: dict[str, type]
    ) -> None:
        if not filename:
            raise ValueError("No configuration file provided")
        self.__file: str = filename
        self.__config: Config = Config()
        self.__filecontent: str = ""

        self.__read_file()
        self.__parsing()

        try:
            ConfigManager._evaluation(self.__config, generators, solvers)
        except ConfigError as e:
            print(f"Config Error caugth: {e}")
            print("Using default value")
            self.__config = ConfigManager._to_default_value()

        except Exception as e:
            print(f"Unexpected Error: {e}")

    def __read_file(self) -> None:
        try:
            with open(self.__file, "r") as f:
                self.__filecontent = f.read()

        except PermissionError:
            print(f"Permission error on {self.__file}")

        except FileNotFoundError:
            print(f"File {self.__file} not found")

        except IsADirectoryError:
            print(f"'{self.__file}' is a directory")

        except Exception as e:
            print(f"Unexpected Error: {e}")

    def __parsing(self) -> None:
        try:
            lines: list[str] = self.__filecontent.splitlines()

            for line in lines:
                line = line.split("#", 1)[0].strip()

                if not line:
                    continue

                key, value = map(str.strip, line.split("=", 1))
                key = ConfigManager.normalize_str(key)

                self.__apply_config(key, value)

        except ConfigError as e:
            print(f"Config Error: {e}")
            print("Merge to default configuration")
            self.__config = ConfigManager._to_default_value()

        except Exception as e:
            print(f"Unexpected Error: {e}")

    @staticmethod
    def normalize_str(val: str) -> str:
        return val.strip().lower()

    def __apply_config(self, key: str, value: str) -> None:
        try:
            if key == "width":
                self.__config.set_width(int(value))

            elif key == "height":
                self.__config.set_height(int(value))

            elif key == "entry":
                self.__config.set_entry(ConfigManager.parse_tuple(value))

            elif key == "exit":
                self.__config.set_exit(ConfigManager.parse_tuple(value))

            elif key == "output_file":
                self.__config.set_output_file(value)

            elif key == "perfect":
                self.__config.set_perfect(ConfigManager.parse_bool(value))

            elif key == "seed":
                self.__config.set_seed(value)

            elif key == "entry":
                self.__config.set_entry(ConfigManager.parse_tuple(value))

            elif key == "exit":
                self.__config.set_exit(ConfigManager.parse_tuple(value))

            elif key == "generator":
                self.__config.set_generator(value)

            elif key == "solver":
                self.__config.set_solver(value)

            elif key == "visual":
                self.__config.set_visual(value)

            else:
                raise ConfigError(f"Unknown key value: {key} - {value}")

        except Exception as e:
            raise ConfigError(e)

    @staticmethod
    def parse_tuple(value: str) -> tuple[int, int]:
        parts: list[str] = value.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid coordinate format: {value}")
        return (int(parts[0]), int(parts[1]))

    @staticmethod
    def parse_bool(value: str) -> bool:
        value = value.strip()
        if value in ("1", "true", "True", "TRUE", "yes", "Yes", "YES"):
            return True
        if value in ("0", "false", "False", "FALSE", "no", "No", "NO"):
            return False
        raise ValueError(f"Invalid boolean format: {value}")

    @classmethod
    def _to_default_value(cls) -> Config:
        return Config()

    def get_config(self) -> dict[str, Any]:
        return self.__config.get_config()

    @classmethod
    def _evaluation(
        cls,
        config: Config,
        generators: dict[str, type],
        solvers: dict[str, type]
    ) -> None:
        conf = config.get_config()

        entry_point = conf["entry"]
        exit_point = conf["exit"]

        width = conf["width"]
        height = conf["height"]

        if width < Pattern42._CELL_WIDTH or height < Pattern42._CELL_HEIGHT + 1:
            raise ConfigError("Size to small for 42 pattern")

        if entry_point == exit_point:
            raise ConfigError("Entry and exit can't be the same")

        if (entry_point[0] > width - 1 or entry_point[1] > height - 1):
            raise ConfigError(f"Entry point out of bound {entry_point}")

        if (exit_point[0] > width - 1 or exit_point[1] > height - 1):
            raise ConfigError(f"Exit point out of bound {exit_point}")

        if Pattern42.is_42_position(entry_point, width, height):
            raise ConfigError("Entry point collide with 42 pattern")

        if Pattern42.is_42_position(exit_point, width, height):
            raise ConfigError("Exit point collide with 42 pattern")

        if (
            conf["generator"] not in generators and
            conf["generator"].lower() != "auto"
        ):
            raise ConfigError(f"Generator {conf['generator']} Unknown")

        if (
            conf["solver"] not in solvers and
            conf["solver"].lower() != "auto"
        ):
            raise ConfigError(f"Solver {conf['solver']} Unknown")
