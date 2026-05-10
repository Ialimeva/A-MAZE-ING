class RegistryError(Exception):
    pass


class GeneratorRegistry:
    _algorithms: dict[str, type] = {}

    @classmethod
    def register(
        cls,
        name: str,
        algorithm: type
    ) -> None:
        if name in cls._algorithms:
            raise RegistryError(
                f"Generator {name} already register as an algorithm typle {algorithm} - "
                "Please choose another name"
            )

        cls._algorithms[name] = algorithm

    @classmethod
    def get(cls, name: str) -> type:
        if name not in cls._algorithms:
            raise RegistryError(f"Generator {name} not found/register")

        return cls._algorithms[name]

    @classmethod
    def avaliable(cls) -> dict[str, type]:
        return cls._algorithms


class SolverRegistry:
    _algorithms: dict[str, type] = {}

    @classmethod
    def register(
        cls,
        name: str,
        algorithm: type
    ) -> None:
        if name in cls._algorithms:
            raise RegistryError(
                f"Solver {name} already register as an algorithm typle {algorithm} - "
                "Please choose another name"
            )

        cls._algorithms[name] = algorithm

    @classmethod
    def get(cls, name: str) -> type:
        if name not in cls._algorithms:
            raise RegistryError(f"Solver {name} not found/register")

        return cls._algorithms[name]

    @classmethod
    def avaliable(cls) -> dict[str, type]:
        return cls._algorithms

