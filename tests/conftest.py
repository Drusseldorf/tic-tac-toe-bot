from unittest.mock import Mock
import pytest


@pytest.fixture
def mock_gameboard(request):
    board = request.param
    mock_game_board = Mock()
    mock_game_board.game_board = board
    return mock_game_board
