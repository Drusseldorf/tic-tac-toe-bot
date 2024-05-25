from game_core.cells import Cell


class GameBoardsToMakeMove:

    BOARD_0_0_IS_OCCUPIED = [
        [Cell.CROSS, Cell.EMPTY, Cell.EMPTY],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY]
    ]

    BOARD_0_0_IS_EMPTY_ZERO_TURN = [
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.CROSS, Cell.EMPTY],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY]
    ]

    BOARD_0_0_IS_EMPTY_CROSS_TURN = [
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.CROSS, Cell.ZERO],
        [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY]
    ]
