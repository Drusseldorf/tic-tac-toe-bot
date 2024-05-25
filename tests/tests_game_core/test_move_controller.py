import pytest
from assertpy import assert_that
from exceptions.illegal_move import IllegalMove
from game_core.cells import Cell
from tests.data.gameboards_to_make_move import GameBoardsToMakeMove
from game_core.move_controller import MoveController


class TestMoveController:

    @pytest.mark.parametrize('mock_gameboard, expected_result', [
        (GameBoardsToMakeMove.BOARD_0_0_IS_OCCUPIED, False),
        (GameBoardsToMakeMove.BOARD_0_0_IS_EMPTY_ZERO_TURN, True),
        (GameBoardsToMakeMove.BOARD_0_0_IS_EMPTY_CROSS_TURN, False)
    ], indirect=['mock_gameboard'])
    def test_move_controller(self, mock_gameboard, expected_result):
        """
        Zero is trying to make move at position 0,0
        1. Position is already occupied, exception raised
        2. Move is possible
        3. Posotion is empty, but it is Cross turn, exception raised
        """
        move_controller = MoveController(mock_gameboard)
        try:
            move_controller.make_move(0, 0, Cell.ZERO)
            is_move_result_success = True
        except IllegalMove:
            is_move_result_success = False

        assert_that(is_move_result_success).is_equal_to(expected_result)
