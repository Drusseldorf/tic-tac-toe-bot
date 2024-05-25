from typing import Dict
from game_core.cells import Cell
from abc import ABC, abstractmethod


class CellMapping(ABC):
    """Custom emojis for players"""
    def __init__(self, mapping_dict: Dict[Cell, str]):
        self._mapping_dict = mapping_dict

    @abstractmethod
    def get_mapped_cell(self, cell: Cell) -> str:
        return self._mapping_dict[cell]
