"""Public package interface.

This package exposes the primary classes required to configure and run
the maze visualization application.

Exports:
    Game: Main application controller responsible for maze generation,
        rendering, solving, and user interaction.
    DisplayConfig: Rendering and display configuration container.
"""

from .display_config import DisplayConfig
from .maze_level import Game

__all__ = [
    "Game",
    "DisplayConfig",
]
