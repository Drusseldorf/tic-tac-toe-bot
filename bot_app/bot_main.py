from bot_app import bot
from bot_app.bot_utils.general_utils.game_session_controller import GameSessionController
from bot_app.bot_utils.general_utils.render_field import RenderManager
from bot_app.bot_utils.general_utils.move_handler import MoveHandler, MoveResult
from data_base.db_utils.session import Session
from bot_app.bot_utils.time_out_session_controller.check_timeout import expires_session_worker
from bot_app.bot_utils.general_utils.no_session_handler import NoSessionHandler
from exceptions.session_not_exists import SessionDoesntExist
from bot_app.bot_utils.online_utils.invite_handler import InitiateInvite
from bot_app.bot_utils.online_utils.invite_sender import InviteSender
from bot_app.bot_utils.general_utils.callback_flags import CallBack
from bot_app.bot_utils.online_utils.linked_accs_session_controller import LinkedAccountsSessionController as Linkcontroller
from bot_app.bot_utils.online_utils.answer_handler import AnswerHandler


@bot.message_handler(commands=['single_game'])
def start_new_game_session(message):
    game_session = Session.new(user1_id=message.from_user.id,
                               user1_chat_id=message.chat.id,
                               is_online=False)
    RenderManager(game_session).render()


@bot.message_handler(commands=['online_game'])
def start_new_online_game_session(message):
    link_session_controller = Linkcontroller(message.from_user.id)
    invite = InitiateInvite(link_session_controller.get_session())
    invite.event_handle(message)


@bot.callback_query_handler(func=lambda call: CallBack.INVT_FLAG.name in call.data)
def invite_send(call):
    linked_user, initiator_user_name, initiator_user_chat_id, _ = call.data.split()
    invite_sender = InviteSender(linked_user, initiator_user_name, initiator_user_chat_id)
    invite_sender.event_handle()


@bot.callback_query_handler(func=lambda call: CallBack.ANSWR_FLAG.name in call.data)
def answer_handler(call):
    answer, initiator_user_chat_id, linked_user_id, _ = call.data.split()
    answer_hndl = AnswerHandler(answer, initiator_user_chat_id, linked_user_id)
    if answer_hndl.handle_answer_is_agree():
        game_session = Session.new(user1_id=initiator_user_chat_id,
                                   user1_chat_id=initiator_user_chat_id,
                                   user2_id=linked_user_id,
                                   user2_chat_id=linked_user_id,
                                   is_online=True)
        RenderManager(game_session).render()


@bot.callback_query_handler(func=lambda call: CallBack.MOVE_FLAG.name in call.data)
def move_callback_handler(call):
    pos_x, pos_y, session_id, _ = call.data.split()
    session_controller = GameSessionController(session_id)

    try:
        game_session = session_controller.get_session()
    except SessionDoesntExist:
        NoSessionHandler(call.message.chat.id, call.message.message_id).inform_no_session()
        return

    move = MoveHandler(pos_x, pos_y, call.from_user.id, game_session)
    if move.make_move() is MoveResult.SUCCESS:
        RenderManager(game_session).render()


if __name__ == '__main__':

    expires_session_worker()
    bot.polling(non_stop=True)
