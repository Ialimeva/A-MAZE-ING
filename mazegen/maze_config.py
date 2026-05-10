from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class MazeConfig:
    width: int
    height: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    perfect: bool
    seed: Optional[int] = None
    grid: Optional[list[list[int]]] = None
