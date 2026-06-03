"""Registry for maze generation and solving algorithms."""


class RegistryError(Exception):
    """Error raised when registry operation fails."""
    pass


class GeneratorRegistry:
    """Registry for maze generator algorithms."""

    _algorithms: dict[str, type] = {}

    @classmethod
    def register(
        cls,
        name: str,
        algorithm: type
    ) -> None:
        """Register a maze generator algorithm.

        Args:
            name: Algorithm identifier.
            algorithm: Generator class.

        Raises:
            RegistryError: If name already registered.
        """
        if name in cls._algorithms:
            raise RegistryError(
                f"Generator {name} already register as an algorithm "
                f"type {algorithm} - "
                "Please choose another name"
            )

        cls._algorithms[name] = algorithm

    @classmethod
    def get(cls, name: str) -> type:
        """Get a registered generator by name.

        Args:
            name: Algorithm identifier.

        Returns:
            Generator class.

        Raises:
            RegistryError: If name not found.
        """
        if name not in cls._algorithms:
            raise RegistryError(f"Generator {name} not found/register")

        return cls._algorithms[name]

    @classmethod
    def avaliable(cls) -> dict[str, type]:
        """Return all registered generators."""
        return cls._algorithms


class SolverRegistry:
    """Registry for maze solver algorithms."""

    _algorithms: dict[str, type] = {}

    @classmethod
    def register(
        cls,
        name: str,
        algorithm: type
    ) -> None:
        """Register a maze solver algorithm.

        Args:
            name: Algorithm identifier.
            algorithm: Solver class.

        Raises:
            RegistryError: If name already registered.
        """
        if name in cls._algorithms:
            raise RegistryError(
                f"Solver {name} already register as an algorithm "
                f"type {algorithm} - "
                "Please choose another name"
            )

        cls._algorithms[name] = algorithm

    @classmethod
    def get(cls, name: str) -> type:
        """Get a registered solver by name.

        Args:
            name: Algorithm identifier.

        Returns:
            Solver class.

        Raises:
            RegistryError: If name not found.
        """
        if name not in cls._algorithms:
            raise RegistryError(f"Solver {name} not found/register")

        return cls._algorithms[name]

    @classmethod
    def avaliable(cls) -> dict[str, type]:
        """Return all registered solvers."""
        return cls._algorithms
