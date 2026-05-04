# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  window.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 11:42:50 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/04 09:43:42 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from typing import Any
from ..utils import MlxApp, MlxPtr, WindowPtr
from ..config import maze_config
from .input_manager import Hooks

class Window():
    def __init__(self):
        self.m: MlxApp = Mlx()
        self.mlx_ptr: MlxPtr = self.m.mlx_init()
        self.win_ptr: WindowPtr = self.m.mlx_new_window(
                        self.mlx_ptr,
                        maze_config["colums"] * maze_config["cell_width"],
                        maze_config["rows"] * maze_config["cell_height"],
                        "A-maze-ing"
        )

        self.m.mlx_hook(self.win_ptr, 2, 1, Hooks.key_pressed, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.exit_window, None)
        
    def start(self, update) -> None:
        self.m.mlx_loop_hook(self.mlx_ptr, update, None)
        self.m.mlx_loop(self.mlx_ptr)

    def exit_window(self, param: Any) -> None:
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)