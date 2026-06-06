class Keymap:
    SPACE = 0x20
    ESC = 0xFF1B
    ENTER = 0xFF0D
    S = 0x73
    P = 0x70
    G = 0x67
    C = 0x63
    E = 0x65
    UP = 0xff52
    DOWN = 0xff54
    LEFT = 0xff51
    RIGHT = 0xff53

    @classmethod
    def get(cls, key: str) -> int | str:
        return getattr(cls, key.upper(), "Unknown key")
