"""Maze rendering module.

This module defines the Draw class, which is responsible for rendering
maze cells, walls, sprites, paths, and themes onto image buffers.

The renderer uses NumPy arrays as image buffers and performs direct
pixel manipulation to generate the final display image presented by
the window system.
"""

import sys
try:
    import numpy as np
except ImportError:
    print("Error: 'numpy' is not installed")
    sys.exit(1)

import random
from ..display_config import DisplayConfig
from .spritsheet import Spritesheet
from .renderer_utils import (
    scale_pixel,
    recolor_pixel,
    tileset,
    floor_colors,
    wall_colors,
    background_colors
)
from typing import Any


class Draw:
    """Maze renderer.

    This class manages sprite extraction, theme application, maze
    rendering, path visualization, and presentation of rendered
    images to the display buffer.

    It operates on image buffers supplied by the window system and
    performs rendering through direct NumPy array manipulation.

    Attributes:
        display_configs: Display configuration settings.
        maze_hex: Maze representation using hexadecimal
            wall encodings.
        path: Solution path coordinates.
        theme_cache: Cached themed sprites and colors.
        active_theme: Currently selected theme.
        camera_x: Horizontal camera offset.
        camera_y: Vertical camera offset.
        speed: Camera movement speed.
    """

    def __init__(
        self,
        img_data: tuple[Any, bytearray, int, int, int],
        buff_data: tuple[Any, bytearray, int, int, int],
        display_data: tuple[Any, bytearray, int, int, int],
        display_configs: DisplayConfig,
    ) -> None:
        """Initialize the renderer.

        Loads sprites from the tileset, creates rendering buffers,
        initializes themes, and prepares rendering resources.

        Args:
            img_data: Tileset image data and metadata.
            buff_data: Maze rendering buffer data and metadata.
            display_data: Display buffer data and metadata.
            display_configs: Display configuration settings.
        """
        self.display_configs = display_configs

        self.img_ptr, self.img_adr, self.img_line, _, _ = img_data
        _, _, _, self.img_width, self.img_height = img_data

        self.buff_ptr, self.buff_adr, self.buff_line, _, _ = buff_data
        _, _, _, self.buff_width, self.buff_height = buff_data

        self.display_ptr, self.display_adr, self.display_line, _, _ = (
            display_data
        )
        _, _, _, self.display_width, self.display_height = display_data

        self.img_array = np.frombuffer(self.img_adr, dtype=np.uint8)
        self.buff_array = np.frombuffer(self.buff_adr, dtype=np.uint8)
        self.display_array = np.frombuffer(self.display_adr, dtype=np.uint8)

        self.img_3d = self.img_array.reshape(
                                    self.img_height,
                                    self.img_width,
                                    4
                                )
        self.buff_3d = self.buff_array.reshape(
                                    self.buff_height,
                                    self.buff_width,
                                    4
                                )

        self.display_3d = self.display_array.reshape(
                                    self.display_height,
                                    self.display_width,
                                    4
                                )

        self.spritesheet = Spritesheet(self.img_3d)
        self.h_wall, self.h_wall_height, self.h_wall_width = tileset(
            self.display_configs.horizontal_wall_x,
            self.display_configs.horizontal_wall_y,
            self.spritesheet
        )

        self.v_wall, self.v_wall_height, self.v_wall_width = tileset(
            self.display_configs.vertical_wall_x,
            self.display_configs.vertical_wall_y,
            self.spritesheet
        )

        self.b_wall, self.b_wall_height, self.b_wall_width = tileset(
            self.display_configs.bottom_wall_x,
            self.display_configs.bottom_wall_y,
            self.spritesheet
        )

        self.sv_wall, self.sv_wall_height, self.sv_wall_width = tileset(
            self.display_configs.side_v_wall_x,
            self.display_configs.side_v_wall_y,
            self.spritesheet
        )

        self.h_joint, self.h_joint_height, self.h_joint_width = tileset(
            self.display_configs.horizontal_joint_x,
            self.display_configs.horizontal_joint_y,
            self.spritesheet
        )

        self.empty_joint, self.empty_joint_height, self.empty_joint_width = (
            tileset(
                self.display_configs.empty_joint_x,
                self.display_configs.empty_joint_y,
                self.spritesheet
            )
        )

        self.dude, self.dude_height, self.dude_width = tileset(
            self.display_configs.dude_x,
            self.display_configs.dude_y,
            self.spritesheet
        )
        self.money, self.money_height, self.money_width = tileset(
            self.display_configs.money_x,
            self.display_configs.money_y,
            self.spritesheet
        )

        self.dude = scale_pixel(self.dude, 2)
        self.dude_height, self.dude_width, _ = self.dude.shape

        self.money = scale_pixel(self.money, 2)
        self.money_height, self.money_width, _ = self.money.shape

        self.maze_hex: list[list[str]] = []
        self.path: list[tuple[int, int]] = []

        self.theme_cache: dict[str, dict[str, Any]] = {}
        self.fcolors = floor_colors
        self.wcolors = wall_colors
        self.bcolors = background_colors
        self.wcolors_keys = list(self.wcolors.keys())

        for theme in self.wcolors_keys:
            w1, w2, w3 = self.wcolors[theme]
            f1, f2, f3 = self.fcolors[theme]
            bcolor = self.bcolors[theme]

            t_hw = self.h_wall.copy()
            t_vw = self.v_wall.copy()
            t_svw = self.sv_wall.copy()
            t_bw = self.b_wall.copy()
            t_hj = self.h_joint.copy()
            t_ej = self.empty_joint.copy()

            for sprite in [t_hw, t_vw, t_svw, t_bw, t_hj, t_ej]:
                recolor_pixel(sprite, [53, 40, 66, 255], w1)
                recolor_pixel(sprite, [23, 17, 28, 255], w2)
                recolor_pixel(sprite, [96, 103, 117, 255], w3)

            self.theme_cache[theme] = {
                "h_wall": t_hw,
                "v_wall": t_vw,
                "b_wall": t_bw,
                "sv_wall": t_svw,
                "hj_wall": t_hj,
                "ej_wall": t_ej,
                "f1": f1,
                "f2": f2,
                "f3": f3,
                "bcolor": bcolor,
            }

        self.active_theme: dict[str, Any] = self.theme_cache["default_theme"]
        self.h_wall, self.v_wall, self.b_wall = (
            self.active_theme["h_wall"],
            self.active_theme["v_wall"],
            self.active_theme["b_wall"]
        )
        self.sv_wall, self.h_joint, self.empty_joint = (
            self.active_theme["sv_wall"],
            self.active_theme["hj_wall"],
            self.active_theme["ej_wall"],
        )
        self.fcolor1, self.fcolor2, self.fcolor3, self.bcolor = (
            self.active_theme["f1"],
            self.active_theme["f2"],
            self.active_theme["f3"],
            self.active_theme["bcolor"]
        )

        self.camera_x, self.camera_y = (0, 0)
        self.speed = 20

    def blit(
            self,
            y_coords: tuple[int, int],
            x_coords: tuple[int, int],
            wall: np.ndarray
    ) -> None:
        """Copy pixel data into the rendering buffer.

        Writes a sprite or color block into the specified region of the
        maze buffer.

        Args:
            y_coords: Vertical destination bounds.
            x_coords: Horizontal destination bounds.
            wall: Sprite or pixel data to copy.
        """
        start_x, end_x = x_coords
        start_y, end_y = y_coords

        self.buff_3d[start_y:end_y, start_x:end_x] = wall

    def floor(self) -> None:
        """Render maze floor tiles.

        Fills each maze cell with the appropriate floor color based on
        its encoded cell type.
        """
        dest_y: int = 0
        for y in range(len(self.maze_hex)):
            dest_x: int = 0
            for x in range(len(self.maze_hex[0])):
                hex_value: str = self.maze_hex[y][x]
                if (hex_value == "F"):
                    self.blit(
                        (dest_y, dest_y + self.display_configs.cell_height),
                        (dest_x, dest_x + self.display_configs.cell_width),
                        self.fcolor2
                    )
                else:
                    self.blit(
                        (dest_y, dest_y + self.display_configs.cell_height),
                        (dest_x, dest_x + self.display_configs.cell_width),
                        self.fcolor1
                    )
                dest_x = dest_x + self.display_configs.cell_width
            dest_y = dest_y + self.display_configs.cell_height

    def cell(self) -> None:
        """Render maze walls and joints.

        Draws all maze walls, corner joints, border walls, and bottom
        boundaries using the currently active theme.
        """
        dest_y = 0
        for y in range(len(self.maze_hex)):
            dest_x = 0
            for x in range(len(self.maze_hex[0])):
                hex_value = int(self.maze_hex[y][x], 16)

                if (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.v_wall_height),
                        (dest_x, dest_x + self.v_wall_width),
                        self.v_wall
                    )

                if (hex_value & 1):
                    self.blit(
                        (dest_y, dest_y + self.h_wall_height),
                        (dest_x + self.v_wall_width,
                         dest_x + self.v_wall_width + self.h_wall_width),
                        self.h_wall
                    )

                if (hex_value & 1) and not (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.h_joint_height),
                        (dest_x, dest_x + self.h_joint_width),
                        self.h_joint
                    )

                if not (hex_value & 1) and not (hex_value >> 3 & 1):
                    self.blit(
                        (dest_y, dest_y + self.empty_joint_height),
                        (dest_x, dest_x + self.empty_joint_width),
                        self.empty_joint
                    )

                if (x == len(self.maze_hex[0]) - 1):
                    self.blit(
                        (dest_y, dest_y + self.v_wall_height),
                        (dest_x + self.v_wall_width + self.h_wall_width,
                         dest_x + self.v_wall_width * 2 + self.h_wall_width),
                        self.v_wall
                    )

                if (y == len(self.maze_hex) - 1):
                    # Draw bottom walls
                    self.blit(
                        (dest_y + self.sv_wall_height - self.h_joint_height,
                         dest_y + self.sv_wall_height + self.h_joint_height),
                        (dest_x, dest_x + self.h_joint_width),
                        self.h_joint
                    )

                    self.blit(
                        (dest_y + self.sv_wall_height - self.b_wall_height,
                         dest_y + self.sv_wall_height + self.b_wall_height),
                        (dest_x + self.v_wall_width,
                         dest_x + self.v_wall_width + self.b_wall_width),
                        self.b_wall
                    )

                    if (x == len(self.maze_hex[0]) - 1):
                        self.blit(
                            (dest_y, dest_y + self.sv_wall_height),
                            (dest_x + self.v_wall_width + self.h_wall_width,
                             dest_x + self.v_wall_width*2 + self.h_wall_width),
                            self.sv_wall
                        )

                dest_x = dest_x + self.v_wall_width + self.h_wall_width
            dest_y = dest_y + self.v_wall_height

    def entry_and_exit(self) -> None:
        """Render entry and exit markers.

        Draws the player sprite at the maze entry point and the goal
        sprite at the maze exit point.
        """
        entry_x, entry_y = self.display_configs.entry_point
        exit_x, exit_y = self.display_configs.exit_point

        dest_entry_x = entry_x * self.display_configs.cell_width
        dest_entry_y = entry_y * self.display_configs.cell_height

        dest_exit_x = exit_x * self.display_configs.cell_width
        dest_exit_y = exit_y * self.display_configs.cell_height

        self.blit(
            (dest_entry_y + 10, dest_entry_y + self.dude_height + 10),
            (dest_entry_x + 12, dest_entry_x + self.dude_width + 12),
            self.dude
        )

        self.blit(
            (dest_exit_y + 10, dest_exit_y + self.money_height + 10),
            (dest_exit_x + 12, dest_exit_x + self.money_width + 12),
            self.money
        )

    def render_path(self) -> None:
        """Render the maze solution path.

        Highlights all coordinates belonging to the current solution
        path and redraws walls above the path overlay.
        """
        for coord in self.path:
            x, y = coord

            dest_x = x * self.display_configs.cell_width
            dest_y = y * self.display_configs.cell_height

            self.blit(
                (dest_y, dest_y + self.display_configs.cell_height),
                (dest_x, dest_x + self.display_configs.cell_width),
                self.fcolor3
            )
        self.cell()

    def maze(self) -> None:
        """Render the complete maze.

        Draws floor tiles followed by wall structures.
        """
        self.floor()
        self.cell()

    def change_wall_color(self) -> None:
        """Switch to a random rendering theme.

        Selects a new theme from the available theme cache and updates
        all active wall, floor, and background colors.
        """
        key = random.choice(self.wcolors_keys)
        while self.active_theme is self.theme_cache[key]:
            key = random.choice(self.wcolors_keys)
        self.active_theme = self.theme_cache[key]

        self.h_wall, self.v_wall, self.b_wall = (
            self.active_theme["h_wall"],
            self.active_theme["v_wall"],
            self.active_theme["b_wall"]
        )
        self.sv_wall, self.h_joint, self.empty_joint = (
            self.active_theme["sv_wall"],
            self.active_theme["hj_wall"],
            self.active_theme["ej_wall"],
        )
        self.fcolor1, self.fcolor2, self.fcolor3, self.bcolor = (
            self.active_theme["f1"],
            self.active_theme["f2"],
            self.active_theme["f3"],
            self.active_theme["bcolor"]
        )

    def present(self) -> None:
        """Compose the final display image.

        Copies the visible portion of the maze buffer into the display
        buffer while applying camera offsets and centering logic.
        """
        self.display_3d[:] = self.bcolor

        visible_h = min(self.buff_height, self.display_height)
        visible_w = min(self.buff_width, self.display_width)

        offset_x = max(0, (self.display_width - self.buff_width) // 2)
        offset_y = max(0, (self.display_height - self.buff_height) // 2)

        self.camera_x = max(0, min(
                self.camera_x, self.buff_width - self.display_width
            )
        )
        self.camera_y = max(0, min(
                self.camera_y, self.buff_height - self.display_height
            )
        )

        self.display_3d[
            offset_y:offset_y + visible_h,
            offset_x:offset_x + visible_w
        ] = self.buff_3d[
            self.camera_y:self.camera_y + visible_h,
            self.camera_x:self.camera_x + visible_w,
        ]
