from bot_app import bot
from bot_app.bot_utils.render_manager import RenderManager
from exceptions.illegal_move import IllegalMove
from data_base.db_utils.session import Session
from exceptions.session_is_over import SessionIsOver
from game_utils.move_handler import Move


@bot.message_handler(commands=['new_game', 'start'])
def start_new_game_session(message):

    session_id = Session.new(message.chat.id)

    render_field(message, session_id)


@bot.message_handler(commands=['online_game'])
def start_new_online_game_session(message):
    pass


def render_field(message, session_id):

    game_board = Session.get_board(session_id)

    field = RenderManager(session_id=session_id,
                          chat_id=message.chat.id,
                          game_board=game_board)
    field.render()


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    pos_x, pos_y, session_id = call.data.split()

    try:
        board = Session.get_board(session_id)
    except SessionIsOver:
        return

    move = Move(board)

    try:
        new_board = move.make(pos_x, pos_y)
    except IllegalMove:
        return

    Session.update_board(session_id, new_board)
    render_field(call.message, session_id)


bot.polling(none_stop=True)
