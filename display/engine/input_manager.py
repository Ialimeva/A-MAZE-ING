# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 13:14:59 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/04 17:32:01 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from .keymap import Keymap

input_manager: dict[str, bool] = {
    "ESC": False,
    "ENTER": False,
}


class Hooks():
    @staticmethod
    def key_pressed(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            input_manager["ESC"] = True
        if keycode == Keymap.get("enter"):
            input_manager["ENTER"] = True


    @staticmethod
    def key_released(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            input_manager["ESC"] = False