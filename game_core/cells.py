from enum import Enum
from config.basic_config import settings


class Cell(Enum):
    EMPTY = settings.game_settings.default_cells.empty_emoji
    CROSS = settings.game_settings.default_cells.cross_emoji
    ZERO = settings.game_settings.default_cells.zero_emoji
