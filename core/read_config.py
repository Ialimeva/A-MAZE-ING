"""Load, parse, and validate maze configuration files.

This module provides classes for storing configuration values and
building validated configurations from text files.
"""

from typing import Optional
from .forty_two_pattern import Pattern42
from typing import Any


class ConfigError(Exception):
    """Raise when an invalid configuration value is encountered."""

    pass


class Config:
    """Store maze configuration values."""

    def __init__(self) -> None:
        """Initialize the configuration with default values."""
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
        self.__story: bool = True

    def get_config(self) -> dict[str, Any]:
        """Return the current configuration.

        Returns:
            A dictionary containing all configuration values.
        """
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
        config["story"] = self.__story

        return config

    def set_width(self, width: int) -> None:
        """Set the maze width.

        Args:
            width: Width of the maze.

        Raises:
            ConfigError: If the width is outside the valid range.
        """
        if width <= 0 or width > 200:
            raise ConfigError(f"Invalid width value: {width}")
        self.__width = width

    def set_height(self, height: int) -> None:
        """Set the maze height.

        Args:
            height: Height of the maze.

        Raises:
            ConfigError: If the height is outside the valid range.
        """
        if height <= 0 or height > 200:
            raise ConfigError(f"Invalid height value {height}")
        self.__height = height

    def set_entry(self, entry: tuple[int, int]) -> None:
        """Set the entry point.

        Args:
            entry: Entry coordinates.

        Raises:
            ConfigError: If the coordinates are invalid.
        """
        if entry[0] < 0 or entry[1] < 0:
            raise ConfigError(f"Invalid entry point value {entry}")
        self.__entry = entry

    def set_exit(self, exit_: tuple[int, int]) -> None:
        """Set the exit point.

        Args:
            exit_: Exit coordinates.

        Raises:
            ConfigError: If the coordinates are invalid.
        """
        if exit_[0] < 0 or exit_[1] < 0:
            raise ConfigError(f"Invalid exit point value {exit_}")
        self.__exit = exit_

    def set_output_file(self, output_file: str) -> None:
        """Set the output filename.

        Args:
            output_file: Destination file.

        Raises:
            ConfigError: If the filename is empty.
        """
        if not output_file:
            raise ConfigError("Empty output_file")
        self.__output_file = output_file

    def set_perfect(self, perfect: bool) -> None:
        """Set whether the maze should be perfect.

        Args:
            perfect: Whether to generate a perfect maze.
        """
        self.__perfect = perfect

    def set_seed(self, seed: str | Optional[int] = None) -> None:
        """Set the random seed.

        Args:
            seed: Seed value or ``None``.

        Raises:
            ConfigError: If the seed cannot be converted to an integer.
        """
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
        """Set the maze generator.

        Args:
            value: Name of the generator.
        """
        self.__generator = value.lower()

    def set_solver(self, value: str) -> None:
        """Set the maze solver.

        Args:
            value: Name of the solver.
        """
        self.__solver = value.lower()

    def set_visual(self, value: str) -> None:
        """Set the visualization backend.

        Args:
            value: Visualization mode.

        Raises:
            ConfigError: If the visualization mode is unsupported.
        """
        if not value:
            raise ConfigError(f"Invalid visual value {value}")
        if value.lower() == "mlx":
            self.__visual = "mlx"
        elif value.lower() == "term":
            self.__visual = "term"
        else:
            raise ConfigError(f"Invalid visual value {value}")

    def set_story(self, value: bool) -> None:
        """Set the story mode of the program.

        Args:
            value: Story mode.
        """
        self.__story = value


class ConfigManager:
    """Build and validate configurations from files."""

    def __init__(
        self,
        filename: str,
        generators: dict[str, type],
        solvers: dict[str, type]
    ) -> None:
        """Load and validate a configuration file.

        Args:
            filename: Path to the configuration file.
            generators: Available maze generators.
            solvers: Available maze solvers.

        Raises:
            ValueError: If no filename is provided.
        """
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
        """Parse the configuration file content.

        Each non-empty line is interpreted as a key-value pair.
        Comments beginning with ``#`` are ignored, and missing or
        invalid values cause the configuration to fall back to the
        default settings.
        """
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
        """Normalize a string.

        Args:
            val: String to normalize.

        Returns:
            The normalized string.
        """
        return val.strip().lower()

    def __apply_config(self, key: str, value: str) -> None:
        """Apply a configuration entry to the current configuration.

        The key determines which configuration field is updated,
        while the value is converted to the appropriate type before
        being assigned.

        Args:
            key: Configuration parameter name.
            value: String representation of the parameter value.

        Raises:
            ConfigError: If the key is unknown or the value is invalid.
        """
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

            elif key == "story":
                self.__config.set_story(ConfigManager.parse_bool(value))

            else:
                raise ConfigError(f"Unknown key value: {key} - {value}")

        except Exception as e:
            raise ConfigError(e)

    @staticmethod
    def parse_tuple(value: str) -> tuple[int, int]:
        """Parse a coordinate pair.

        Args:
            value: Coordinate string.

        Returns:
            The parsed coordinates.

        Raises:
            ValueError: If the format is invalid.
        """
        parts: list[str] = value.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid coordinate format: {value}")
        return (int(parts[0]), int(parts[1]))

    @staticmethod
    def parse_bool(value: str) -> bool:
        """Parse a boolean value.

        Args:
            value: Boolean string.

        Returns:
            The corresponding boolean value.

        Raises:
            ValueError: If the value is not recognized.
        """
        value = value.strip()
        if value.lower() in ("1", "true", "yes"):
            return True
        if value.lower() in ("0", "false", "no"):
            return False
        raise ValueError(f"Invalid boolean format: {value}")

    @classmethod
    def _to_default_value(cls) -> Config:
        """Create a configuration initialized with default values.

        Returns:
            A default configuration object.
        """
        return Config()

    def get_config(self) -> dict[str, Any]:
        """Return the validated configuration.

        Returns:
            A dictionary containing the configuration values.
        """
        return self.__config.get_config()

    @classmethod
    def _evaluation(
        cls,
        config: Config,
        generators: dict[str, type],
        solvers: dict[str, type]
    ) -> None:
        """Validate a configuration.

        Args:
            config: Configuration to validate.
            generators: Available maze generators.
            solvers: Available maze solvers.

        Raises:
            ConfigError: If one or more configuration values are invalid.
        """
        conf = config.get_config()

        entry_point = conf["entry"]
        exit_point = conf["exit"]

        width = conf["width"]
        height = conf["height"]

        if (
            width < Pattern42._CELL_WIDTH + 2 or
            height < Pattern42._CELL_HEIGHT + 3
        ):
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
