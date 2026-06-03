"""
    Contain the Register of the created algorithm on both
        Solver and Generator
"""

class RegistryError(Exception):
    """
        Error Raise by all Register
    """
    pass


class GeneratorRegistry:
    """
        Represent the Register of all Generator algorithm when given a name

        Class Attributes:
            _algorithms (dict[str, type])
    """

    _algorithms: dict[str, type] = {}

    @classmethod
    def register(
        cls,
        name: str,
        algorithm: type
    ) -> None:
        """
            Save the given algorithm to the register

            Args:
                name (str): the name-key of the algorithm
                algorithm (type): the class of the algorithm

            Raise:
                RegistryError if name already on the register
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
        """
            Getter of algorithm

            Args:
                name (str): the name-key of the algorithm to get

            Raise:
                RegistryError if name not present in the register

            Return:
                type: The algorithm
        """
        if name not in cls._algorithms:
            raise RegistryError(f"Generator {name} not found/register")

        return cls._algorithms[name]

    @classmethod
    def avaliable(cls) -> dict[str, type]:
        """
            Getter of all register algorithm

            Return:
                dict[str, type]: format key: value -> name: algorithm
        """
        return cls._algorithms


class SolverRegistry:
    """
        Represent the Register of all Solver algorithm when given a name

        Class Attributes:
            _algorithms (dict[str, type])
    """
    _algorithms: dict[str, type] = {}

    @classmethod
    def register(
        cls,
        name: str,
        algorithm: type
    ) -> None:
        """
            Save the given algorithm to the register

            Args:
                name (str): the name-key of the algorithm
                algorithm (type): the class of the algorithm

            Raise:
                RegistryError if name already on the register
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
        """
            Getter of algorithm

            Args:
                name (str): the name-key of the algorithm to get

            Raise:
                RegistryError if name not present in the register

            Return:
                type: The algorithm
        """
        if name not in cls._algorithms:
            raise RegistryError(f"Solver {name} not found/register")

        return cls._algorithms[name]

    @classmethod
    def avaliable(cls) -> dict[str, type]:
        """
            Getter of all register algorithm

            Return:
                dict[str, type]: format key: value -> name: algorithm
        """
        return cls._algorithms
