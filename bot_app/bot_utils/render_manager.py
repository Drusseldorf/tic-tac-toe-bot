from bot_app import bot
from bot_app.bot_utils.cell_image_mapping import Mapping
from game_utils.field import GameBoard
from game_utils.move_handler import Move
from config.text_templates.russian import Text
from data_base.db_utils.session import Session
from game_utils.game_state_handler import State, GameState
from telebot import types


class RenderManager:

    def __init__(self,
                 session_id: str,
                 chat_id: str,
                 game_board: str):
        self._session_id = session_id
        self._mapping_obj = Mapping()
        self._chat_id = chat_id
        self._game_board = GameBoard.turn_into_list(game_board)
        self._whos_turn = Move(game_board).whos_turn()
        self._last_move = Move(game_board).last_turn()

    def _game_board_into_buttons(self):

        buttons = []
        pos_x = 0
        pos_y = 0

        for row in self._game_board:
            pos_x += 1
            for cell in row:
                pos_y += 1
                cell_emoji = self._mapping_obj.cell_into_emoji(cell)
                button = types.InlineKeyboardButton(text=cell_emoji,
                                                    callback_data=f'{pos_x - 1} {pos_y - 1} {self._session_id}')
                buttons.append(button)
            pos_y = 0
        return buttons

    def _check_last_message(self):
        return Session.get_last_message(self._session_id)

    def _game_state(self):
        return GameState(GameBoard.turn_into_str(self._game_board)).state

    def _prepare_buttons(self):
        buttons = self._game_board_into_buttons()
        markup = types.InlineKeyboardMarkup(row_width=len(self._game_board))
        markup.add(*buttons)
        return markup

    def _get_last_move_cell(self):
        return self._mapping_obj.cell_into_emoji(self._last_move)

    def _get_next_move_cell(self):
        return self._mapping_obj.cell_into_emoji(self._whos_turn)

    def _bot_attrbt(self):
        return 'edit_message_text' if self._check_last_message() else 'send_message'

    def _text_attrbt(self):
        if self._game_state() == State.IN_PROGRESS:
            return 'NEXT_TURN'
        elif self._game_state() == State.DRAW:
            return 'DRAW'
        else:
            return 'WON'

    def _text_cell_or_draw(self):
        if self._game_state() == State.IN_PROGRESS:
            return self._get_next_move_cell()
        elif self._game_state() == State.DRAW:
            return ''
        else:
            return self._get_last_move_cell()

    def _message_body(self):
        body = {
            'chat_id': self._chat_id,
            'reply_markup': self._prepare_buttons(),
            'text': f'{getattr(Text, self._text_attrbt())} {self._text_cell_or_draw()}'
        }
        if self._check_last_message():
            body['message_id'] = self._check_last_message()
        return body

    def _game_state_session_control(self, sent):

        if not self._check_last_message():
            Session.set_last_message(self._session_id, sent.message_id)
        if self._check_last_message() and self._game_state() != State.IN_PROGRESS:
            Session.delete_session(self._session_id)

    def render(self):

        sent = getattr(bot, self._bot_attrbt())(**self._message_body())
        self._game_state_session_control(sent)

    def render_online(self):
        pass
