"""Maze solving algorithms."""

from .solver_base import MazeSolver, SolverError
from .algorithms import SolverBFS, SolverDijkstra, SolverAStar


__all__ = [
    "MazeSolver",
    "SolverError",
    "SolverBFS",
    "SolverDijkstra",
    "SolverAStar"
]
