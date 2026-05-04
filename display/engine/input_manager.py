# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  input_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: ialrandr <ialrandr@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/01 13:14:59 by ialrandr        #+#    #+#               #
#  Updated: 2026/05/04 09:34:17 by ialrandr        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from .keymap import Keymap

input_manager: dict[str, bool] = {
    "ESC" : False,
}

class Hooks():
    @staticmethod
    def key_pressed(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            input_manager["ESC"] = True
    
    # @staticmethod
    # def key_released(keycode: int) -> None:
        # if keycode == Keymap.get("esc"):
            # input_manager["ESC"] = True