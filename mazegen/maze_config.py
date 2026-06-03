"""Configuration container for maze generation and solving."""

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class MazeConfig:
    """Configuration data for maze generation and solving.

    Attributes:
        width: Maze width in cells.
        height: Maze height in cells.
        entry_point: Entry coordinate as (x, y).
        exit_point: Exit coordinate as (x, y).
        perfect: Whether maze is perfect (no loops).
        seed: Random seed for reproducibility.
        grid: Pre-initialized grid (optional).
    """
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    perfect: bool
    seed: Optional[int] = None
    grid: Optional[list[list[int]]] = None
