from typing import Any
from .keymap import Keymap


class Hooks():
    input_manager: dict[str, bool] = {
        "ESC": False,
        "ENTER": False,
        "S": False,
        "P": False,
        "G": False,
        "C": False,
        "E": False,
        "UP": False,
        "DOWN": False,
        "LEFT": False,
        "RIGHT": False,
    }

    @staticmethod
    def key_pressed(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            Hooks.input_manager["ESC"] = True

        if keycode == Keymap.get("enter"):
            Hooks.input_manager["ENTER"] = True

        if keycode == Keymap.get("s"):
            Hooks.input_manager["S"] = True

        if keycode == Keymap.get("p"):
            Hooks.input_manager["P"] = True

        if keycode == Keymap.get("g"):
            Hooks.input_manager["G"] = True

        if keycode == Keymap.get("c"):
            Hooks.input_manager["C"] = True

        if keycode == Keymap.get("e"):
            Hooks.input_manager["E"] = True

        if keycode == Keymap.get("up"):
            Hooks.input_manager["UP"] = True

        if keycode == Keymap.get("down"):
            Hooks.input_manager["DOWN"] = True

        if keycode == Keymap.get("left"):
            Hooks.input_manager["LEFT"] = True

        if keycode == Keymap.get("right"):
            Hooks.input_manager["RIGHT"] = True

    @staticmethod
    def key_released(keycode: int, param: Any) -> None:
        if keycode == Keymap.get("esc"):
            Hooks.input_manager["ESC"] = False

        if keycode == Keymap.get("up"):
            Hooks.input_manager["UP"] = False

        if keycode == Keymap.get("down"):
            Hooks.input_manager["DOWN"] = False

        if keycode == Keymap.get("left"):
            Hooks.input_manager["LEFT"] = False

        if keycode == Keymap.get("right"):
            Hooks.input_manager["RIGHT"] = False
