# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  window.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 11:42:50 by ialrandr        #+#    #+#               #
#  Updated: 2026/06/03 12:51:46 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from typing import Any
from ..utils import MlxApp, MlxPtr, WindowPtr, ImagePtr
from ..display_config import DisplayConfig
from .input_manager import Hooks

class Window():
    def __init__(self, display_config: DisplayConfig):
        self.m: MlxApp = Mlx()
        self.mlx_ptr: MlxPtr = self.m.mlx_init()
        self.maze_width: int = (
            display_config.columns * display_config.cell_width +
            display_config.extra_width
        )
        self.maze_height: int = (
            display_config.rows * display_config.cell_height +
            display_config.extra_height
        )
        print(self.maze_height)

        self.display_width = display_config.display_width
        self.display_height = display_config.display_height
        self.win_ptr: WindowPtr = self.m.mlx_new_window(
                        self.mlx_ptr,
                        self.display_width,
                        self.display_height,
                        "A-maze-ing"
        )

        (self.wimg_ptr, _, _) = self.m.mlx_png_file_to_image(
                                    self.mlx_ptr,
                                    "display/assets/A-MAZE-ING.png"
                                )
        
        self.m.mlx_hook(self.win_ptr, 2, 1, Hooks.key_pressed, None)
        self.m.mlx_hook(self.win_ptr, 3, 2, Hooks.key_released, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.exit_window, None)
        
    def start(self, update) -> None:
        self.m.mlx_loop_hook(self.mlx_ptr, update, None)
        self.m.mlx_loop(self.mlx_ptr)

    def exit_window(self, param: Any) -> None:
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)

    def img_data(self) -> tuple:
        (self.img_ptr,
         self.img_width,
         self.img_height
        ) = self.m.mlx_png_file_to_image(
                self.mlx_ptr,
                "display/assets/tileset.png"
            )
        (self.img_adr, _, self.img_line, _) = self.m.mlx_get_data_addr(
                                                self.img_ptr
                                            )
        return (self.img_ptr,
                self.img_adr,
                self.img_line,
                self.img_width,
                self.img_height
            )
    
    def buff_data(self) -> tuple:
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
    
    def display_data(self) -> tuple:
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
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.display_ptr,
            0, 0
        )
    
    def welcome_page(self) -> None:
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.wimg_ptr,
            0, 0
        )
