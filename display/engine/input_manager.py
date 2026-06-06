# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 13:14:59 by ialrandr        #+#    #+#               #
#  Updated: 2026/06/05 10:51:46 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from .keymap import Keymap

input_manager: dict[str, bool] = {
    "ESC": False,
    "ENTER": False,
    "S": False,
    "P": False,
    "G": False,
    "C": False,
    "UP": False,
    "DOWN": False,
    "LEFT": False,
    "RIGHT": False,
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

        if keycode == Keymap.get("p"):
            input_manager["P"] = True

        if keycode == Keymap.get("g"):
            input_manager["G"] = True

        if keycode == Keymap.get("c"):
            input_manager["C"] = True

        if keycode == Keymap.get("up"):
            input_manager["UP"] = True

        if keycode == Keymap.get("down"):
            input_manager["DOWN"] = True

        if keycode == Keymap.get("left"):
            input_manager["LEFT"] = True

        if keycode == Keymap.get("right"):
            input_manager["RIGHT"] = True

    @staticmethod
    def key_released(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            input_manager["ESC"] = False

        if keycode == Keymap.get("up"):
            input_manager["UP"] = False

        if keycode == Keymap.get("down"):
            input_manager["DOWN"] = False

        if keycode == Keymap.get("left"):
            input_manager["LEFT"] = False

        if keycode == Keymap.get("right"):
            input_manager["RIGHT"] = False
