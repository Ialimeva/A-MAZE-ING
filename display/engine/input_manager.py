# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 13:14:59 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/24 13:41:49 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from .keymap import Keymap

input_manager: dict[str, bool] = {
    "ESC": False,
    "ENTER": False,
    "S": False,
    "P": False,
    "H": False,
}


class Hooks():
    @staticmethod
    def key_pressed(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            input_manager["ESC"] = True
        
        if keycode == Keymap.get("enter"):
            input_manager["ENTER"] = True
        
        if keycode == Keymap.get("s"):
            input_manager["S"] = True
        
        if keycode == Keymap.get("h"):
            input_manager["H"] = True


    @staticmethod
    def key_released(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            input_manager["ESC"] = False
        
        # if keycode == Keymap.get("enter"):
        #     input_manager["ENTER"] = False
        
        if keycode == Keymap.get("s"):
            input_manager["S"] = False
        
        if keycode == Keymap.get("h"):
            input_manager["H"] = False