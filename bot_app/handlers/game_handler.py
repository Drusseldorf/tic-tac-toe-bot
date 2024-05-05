from bot_app import bot
from bot_app.bot_utils.session_controller import SessionController
from bot_app.bot_utils.render_field import RenderManager
from bot_app.bot_utils.move_handler import MoveHandler
from data_base.db_utils.session import Session


@bot.message_handler(commands=['new_game', 'start'])
def start_new_game_session(message):
    session_id = Session.new(message.chat.id)
    RenderManager(session_id).render()


@bot.callback_query_handler(func=lambda call: True)
def move_callback_handler(call):

    pos_x, pos_y, session_id = call.data.split()

    session_controller = SessionController(session_id)
    game_session = session_controller.get_session()

    if game_session:
        MoveHandler(pos_x, pos_y, game_session).make_move()
        RenderManager(session_id).render()


bot.polling(none_stop=True)
