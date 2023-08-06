from enum import Enum

from .color import Color

__all__ = ["ThemeTypes", "SizeTypes", "NamedColor", "KmarkdownColors"]


class ThemeTypes(Enum):
    PRIMARY = "primary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    SECONDARY = "secondary"
    NONE = "none"


class SizeTypes(Enum):
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"


class KmarkdownColors(Enum):
    DANGER = "danger"
    INFO = "info"
    PINK = "pink"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    NONE = "none"


class NamedColor(Enum):
    BLACK = Color(0, 0, 0)
    DARK_BLUE = Color(0, 0, 170)
    DARK_GREEN = Color(0, 170, 0)
    DARK_AQUA = Color(0, 170, 170)
    DARK_RED = Color(170, 0, 0)
    DARK_PURPLE = Color(170, 0, 170)
    GOLD = Color(255, 170, 0)
    GRAY = Color(170, 170, 170)
    DARK_GRAY = Color(85, 85, 85)
    BLUE = Color(85, 85, 255)
    GREEN = Color(85, 255, 85)
    AQUA = Color(85, 255, 255)
    RED = Color(255, 85, 85)
    YELLOW = Color(255, 255, 85)
    WHITE = Color(255, 255, 255)
