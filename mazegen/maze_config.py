"""
    Contain the Configuration contract of the Maze
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class MazeConfig:
    """
        Represent the configuration of the Maze pass generator and solver
        Attributes:
            width (int),
            height (int),
            entry_point (tuple[int, int]),
            exit_point (tuple[int, int])
            perfect (bool)
            seed (Optional[int])
            grid (Optional[list[list[int]]])
    """
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    perfect: bool
    seed: Optional[int] = None
    grid: Optional[list[list[int]]] = None
