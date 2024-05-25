from game_core.cells import Cell


class GameBoardsStates:
    BOARD_GAME_IN_PROGRESS = [
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY]
    ]

    BOARD_GAME_CROSS_WON = [
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.CROSS, Cell.EMPTY]
    ]

    BOARD_GAME_ZERO_WON = [
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.CROSS, Cell.EMPTY, Cell.ZERO]
    ]

    BOARD_GAME_DRAW = [
        [Cell.ZERO, Cell.CROSS, Cell.ZERO],
        [Cell.CROSS, Cell.CROSS, Cell.ZERO],
        [Cell.CROSS, Cell.ZERO, Cell.CROSS]
    ]

    BOARD_GAME_CROSS_WIN_DIAGONAL = [
        [Cell.CROSS, Cell.EMPTY, Cell.ZERO],
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.EMPTY, Cell.CROSS]
    ]