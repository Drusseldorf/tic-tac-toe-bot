from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings_yaml import YamlBaseSettings
import warnings

warnings.filterwarnings('ignore')

ROOT_DIR = Path(__file__).parent.parent
CONFIG_DIR = ROOT_DIR.joinpath('config')

config_file = CONFIG_DIR.joinpath('config.yaml')
env_file = CONFIG_DIR.joinpath('.env')


class BotSettings(BaseModel):
    token: str


class DBSettings(BaseModel):
    url: str


class DefaultCells(BaseModel):
    cross_emoji: str
    zero_emoji: str
    empty_emoji: str


class VictoryConditions(Enum):
    THREE_IN_A_ROW = 3
    FOUR_IN_A_ROW = 4


class GameSettings(BaseModel):
    victory_condition: VictoryConditions
    game_board_default_size: int
    default_cells: DefaultCells


class MainSettings(YamlBaseSettings):
    bot_settings: BotSettings
    game_settings: GameSettings
    db_settings: DBSettings

    class Config:
        yaml_file = config_file
        env_file = env_file
        env_prefix = 'ENV__'
        env_nested_delimiter = '__'


settings = MainSettings()
