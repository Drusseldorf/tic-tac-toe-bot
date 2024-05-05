from telebot import types
from bot_app.bot_utils.cell_image_mapping import Mapping
from config.text_templates.russian import MoveTurnText
from game_utils.field import GameBoard
from game_utils.game_state_handler import State, GameState
from game_utils.make_move import Move


class MessageBuilder:
    def __init__(self, last_message, game_board, session_id):
        self._session_id = session_id
        self._game_board = game_board
        self._last_message = last_message

    def _game_board_into_buttons(self):
        buttons = []
        pos_x = 0
        pos_y = 0
        for row in GameBoard.turn_into_list(self._game_board):
            pos_x += 1
            for cell in row:
                pos_y += 1
                cell_emoji = Mapping.cell_into_emoji(cell)
                button = types.InlineKeyboardButton(text=cell_emoji,
                                                    callback_data=f'{pos_x - 1} {pos_y - 1} {self._session_id}')
                buttons.append(button)
            pos_y = 0
        return buttons

    def _prepare_buttons(self):
        buttons = self._game_board_into_buttons()
        markup = types.InlineKeyboardMarkup(row_width=len(GameBoard.turn_into_list(self._game_board)))
        markup.add(*buttons)
        return markup

    def _text_attrbt(self):
        game_state = GameState(self._game_board).state
        if game_state == State.IN_PROGRESS:
            return 'NEXT_TURN'
        elif game_state == State.DRAW:
            return 'DRAW'
        else:
            return 'WON'

    def _text_cell_or_draw(self):
        move = Move(self._game_board)
        game_state = GameState(self._game_board).state
        if game_state == State.IN_PROGRESS:
            return Mapping.cell_into_emoji(move.whos_turn())
        elif game_state == State.DRAW:
            return ''
        else:
            return Mapping.cell_into_emoji(move.last_turn())

    def message_body(self, chat_id) -> dict:
        last_message_id = self._last_message
        body = {
            'chat_id': chat_id,
            'reply_markup': self._prepare_buttons(),
            'text': f'{getattr(MoveTurnText, self._text_attrbt())} {self._text_cell_or_draw()}'
        }
        if last_message_id:
            body['message_id'] = last_message_id
        return body
