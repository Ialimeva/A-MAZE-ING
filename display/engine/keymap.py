class Keymap:
    ESC = 0xFF1B
    ENTER = 0xFF0D
    S = 0x73
    P = 0x70
    G = 0x67

    @classmethod
    def get(cls, key: str) -> int | str:
        return getattr(cls, key.upper(), "Unknown key")