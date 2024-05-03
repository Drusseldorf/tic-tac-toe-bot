from game_utils.cells import Cell
from config.basic_config import settings


class Mapping:
    def __init__(self, dict_to_map: dict = None):
        if dict_to_map is None:
            dict_to_map = {
                Cell.CROSS: settings.game_settings.default_cells.cross_emoji,
                Cell.ZERO: settings.game_settings.default_cells.zero_emoji,
                Cell.EMPTY: settings.game_settings.default_cells.empty_emoji
            }
        self._defoult_mapping = dict_to_map

    def cell_into_emoji(self, cell: Cell) -> str:
        return self._defoult_mapping[cell]
