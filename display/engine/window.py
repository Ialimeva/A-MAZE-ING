"""Window management module.

This module provides the Window class, which wraps MLX window,
image, and event handling functionality. It is responsible for
creating the application window, loading graphical assets,
managing rendering buffers, and registering input callbacks.
"""

import sys
try:
    from mlx import Mlx
except ImportError:
    print("Error: 'mlx' is not installed")
    sys.exit(1)

from typing import Any
from ..display_config import DisplayConfig
from .input_manager import Hooks


class Window():
    """Application window manager.

    This class encapsulates interactions with the MLX graphics library,
    including window creation, image management, event registration,
    and rendering operations.

    It provides helper methods for loading assets, creating rendering
    buffers, displaying images, and controlling the application's
    event loop.

    Attributes:
        m: MLX wrapper instance.
        mlx_ptr: MLX context pointer.
        win_ptr: Window pointer.
        maze_width: Width of the rendered maze image.
        maze_height: Height of the rendered maze image.
        display_width: Width of the application window.
        display_height: Height of the application window.
    """

    def __init__(self, display_config: DisplayConfig) -> None:
        """Initialize the application window.

        Creates the MLX context, application window, graphical assets,
        and registers keyboard and window event hooks.

        Args:
            display_config: Display configuration used
                to determine maze and window dimensions.
        """
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.maze_width: int = (
            display_config.columns * display_config.cell_width +
            display_config.extra_width
        )
        self.maze_height: int = (
            display_config.rows * display_config.cell_height +
            display_config.extra_height
        )

        self.display_width = display_config.display_width
        self.display_height = display_config.display_height
        self.win_ptr = self.m.mlx_new_window(
                        self.mlx_ptr,
                        self.display_width,
                        self.display_height,
                        "A-maze-ing"
        )
        (self.wimg_ptr, _, _) = self.m.mlx_png_file_to_image(
                                    self.mlx_ptr,
                                    "display/assets/A-MAZE-ING.png"
                                )

        (self.menu_ptr, _, _) = self.m.mlx_png_file_to_image(
                                    self.mlx_ptr,
                                    "display/assets/menu.png"
                                )

        self.m.mlx_hook(self.win_ptr, 2, 1, Hooks.key_pressed, None)
        self.m.mlx_hook(self.win_ptr, 3, 2, Hooks.key_released, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.exit_window, None)

    def start(self, update: Any) -> None:
        """Start the MLX event loop.

        Registers the update callback and begins processing events.

        Args:
            update: Callback executed on each loop iteration.
        """
        self.m.mlx_loop_hook(self.mlx_ptr, update, None)
        self.m.mlx_loop(self.mlx_ptr)

    def exit_window(self, param: Any) -> None:
        """Close the application window and release resources.

        Destroys the MLX window and frees the associated MLX context.

        Args:
            param: Callback parameter supplied by MLX.
                This parameter is not used.
        """
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)

    def img_data(self) -> tuple[Any, bytearray, int, int, int]:
        """Load the tileset image and retrieve image data.

        Loads the tileset texture used for maze rendering and returns
        its associated image buffer information.

        Returns:
            tuple:
                A tuple containing:

                - Image pointer.
                - Image data buffer.
                - Bytes per image row.
                - Image width.
                - Image height.
        """
        self.img_ptr, self.img_width, self.img_height = (
            self.m.mlx_png_file_to_image(
                self.mlx_ptr,
                "display/assets/tileset.png"
            )
        )
        (self.img_adr, _, self.img_line, _) = self.m.mlx_get_data_addr(
                                                self.img_ptr
                                            )
        return (
            self.img_ptr,
            self.img_adr,
            self.img_line,
            self.img_width,
            self.img_height
        )

    def buff_data(self) -> tuple[Any, bytearray, int, int, int]:
        """Create the maze rendering buffer.

        Creates an off-screen image used as the primary rendering target
        for maze graphics.

        Returns:
            tuple:
                A tuple containing:

                - Buffer image pointer.
                - Buffer data buffer.
                - Bytes per image row.
                - Buffer width.
                - Buffer height.
        """
        self.buff_ptr = self.m.mlx_new_image(
                    self.mlx_ptr,
                    self.maze_width,
                    self.maze_height
                )
        self.buff_adr, _, self.buff_line, _ = self.m.mlx_get_data_addr(
                                                self.buff_ptr
                                    )
        return (
            self.buff_ptr,
            self.buff_adr,
            self.buff_line,
            self.maze_width,
            self.maze_height
        )

    def display_data(self) -> tuple[Any, bytearray, int, int, int]:
        """Create the display buffer.

        Creates the image buffer presented directly to the application
        window.

        Returns:
            tuple:
                A tuple containing:

                - Display image pointer.
                - Display data buffer.
                - Bytes per image row.
                - Display width.
                - Display height.
        """
        self.display_ptr = self.m.mlx_new_image(
                    self.mlx_ptr,
                    self.display_width,
                    self.display_height
                )

        self.display_adr, _, self.display_line, _ = self.m.mlx_get_data_addr(
                                                self.display_ptr
                                    )
        return (
            self.display_ptr,
            self.display_adr,
            self.display_line,
            self.display_width,
            self.display_height
        )

    def render_image(self) -> None:
        """Render the display buffer to the application window."""
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.display_ptr,
            0, 0
        )

    def welcome_page(self) -> None:
        """Display the application's welcome screen."""
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.wimg_ptr,
            0, 0
        )

    def put_menu(self) -> None:
        """Display the in-game menu overlay."""
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.menu_ptr,
            0, 0
        )
