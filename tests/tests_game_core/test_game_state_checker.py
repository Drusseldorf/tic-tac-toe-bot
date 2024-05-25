from tests.data.game_boards_states import GameBoardsStates
import pytest as pytest
from config.basic_config import settings
from assertpy import assert_that
from game_core.game_states import State
from game_core.game_state_checker import GameState


class TestGameState:

    @classmethod
    def setup_method(cls):
        """
        Setting gameboard size and victory condition to default
        """
        settings.game_settings.game_board_default_size = 3
        settings.game_settings.victory_condition = 3

    @pytest.mark.parametrize('mock_gameboard, expected_state', [
        (GameBoardsStates.BOARD_GAME_ZERO_WON, State.ZERO_WON),
        (GameBoardsStates.BOARD_GAME_DRAW, State.DRAW),
        (GameBoardsStates.BOARD_GAME_CROSS_WON, State.CROSS_WON),
        (GameBoardsStates.BOARD_GAME_IN_PROGRESS, State.IN_PROGRESS),
        (GameBoardsStates.BOARD_GAME_CROSS_WIN_DIAGONAL, State.CROSS_WON)
    ], indirect=['mock_gameboard'])
    def test_game_state(self, mock_gameboard, expected_state):
        """
        Checks if GameState.state is providing game state as expected
        1. Zero won at row
        2. Draw
        3. Cross won at row
        4. Game in progress
        5. Cross won at diagonal
        """
        state = GameState(mock_gameboard).state

        assert_that(state).is_equal_to(expected_state)
