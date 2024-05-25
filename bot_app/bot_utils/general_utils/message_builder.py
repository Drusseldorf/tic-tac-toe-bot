from typing import List
from telebot import types
import pickle
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.text_templates.text_tamplate_obj import template
from data_base.tables import GameSession
from game_core.game_state_checker import State, GameState
from game_core.move_controller import MoveController
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from bot_app.bot_utils.common_utils import get_name, number_of_chats


class MessageBuilder:
    def __init__(self, game_session: GameSession):
        self._game_session = game_session
        self._game_board_obj = pickle.loads(game_session.game_board)
        self._move_controller = MoveController(self._game_board_obj)

    def message_body(self) -> list[dict]:
        """
        Creates message text and markup
        :return:
            list[dict]: A list of dictionaries, each representing a message body to be sent
        """
        message_bodies = []
        last_messages = (self._game_session.last_message_id_user_one, self._game_session.last_message_id_user_two)
        chat_ids = (self._game_session.user_one_chat_id, self._game_session.user_two_chat_id)

        for i in range(number_of_chats(self._game_session)):
            body = {
                'chat_id': chat_ids[i],
                'reply_markup': self._prepare_buttons(),
                'text': f'{self._get_text()} {self._text_cell_or_draw()}'
            }

            if last_messages[i]:
                body['message_id'] = last_messages[i]

            message_bodies.append(body)

        return message_bodies

    def _game_board_into_buttons(self) -> List[InlineKeyboardButton]:
        buttons = []
        pos_x, pos_y = 0, 0
        for row in self._game_board_obj.game_board:
            pos_x += 1
            for cell in row:
                pos_y += 1
                button = types.InlineKeyboardButton(text=cell.value,
                                                    callback_data=f'{pos_x - 1} '
                                                                  f'{pos_y - 1} '
                                                                  f'{self._game_session.session_uuid} '
                                                                  f'{CallBack.MOVE_FLAG.value}')
                buttons.append(button)
            pos_y = 0
        return buttons

    def _prepare_buttons(self) -> InlineKeyboardMarkup:
        buttons = self._game_board_into_buttons()
        markup = types.InlineKeyboardMarkup(row_width=len(self._game_board_obj.game_board))
        markup.add(*buttons)
        return markup

    def _text_attrbt(self) -> str:
        game_state = GameState(self._game_board_obj).state
        if game_state is State.IN_PROGRESS:
            return 'NEXT_TURN'
        elif game_state is State.DRAW:
            return 'DRAW'
        else:
            return 'WON'

    def _get_current_move_user_name(self):
        user_id = self._get_current_user_id()
        return get_name(user_id)

    def _get_current_user_id(self):
        if GameState(self._game_board_obj).state is not State.IN_PROGRESS:
            last_turn_cell = self._move_controller.last_turn()
            return self._game_session.user_one_id if last_turn_cell is self._game_session.user_one_cell else self._game_session.user_two_id
        else:
            current_turn_cell = self._move_controller.whos_turn()
            return self._game_session.user_one_id if current_turn_cell is self._game_session.user_one_cell else self._game_session.user_two_id

    def _get_text(self):
        if self._game_session.is_online:
            return getattr(template.MOVE_TURN_TEXT_ONLINE, self._text_attrbt()).format(self._get_current_move_user_name())
        else:
            return getattr(template.MOVE_TURN_TEXT, self._text_attrbt())

    def _text_cell_or_draw(self):
        match GameState(self._game_board_obj).state:
            case State.IN_PROGRESS:
                return self._move_controller.whos_turn().value
            case State.DRAW:
                return ''
            case _:
                return self._move_controller.last_turn().value
