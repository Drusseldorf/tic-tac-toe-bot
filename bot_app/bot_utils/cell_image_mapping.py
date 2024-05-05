from game_utils.cells import Cell
from config.basic_config import settings


class Mapping:

    _dict_to_map = {
        Cell.CROSS: settings.game_settings.default_cells.cross_emoji,
        Cell.ZERO: settings.game_settings.default_cells.zero_emoji,
        Cell.EMPTY: settings.game_settings.default_cells.empty_emoji
    }

    @classmethod
    def cell_into_emoji(cls, cell: Cell) -> str:
        return cls._dict_to_map[cell]
