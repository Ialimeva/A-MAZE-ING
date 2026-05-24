class Keymap:
    ESC = 0xFF1B
    ENTER = 0xFF0D
    S = 0x73
    H = 0x68

    @classmethod
    def get(cls, key: str) -> int | str:
        return getattr(cls, key.upper(), "Unknown key")