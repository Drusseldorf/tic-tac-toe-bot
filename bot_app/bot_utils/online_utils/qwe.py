from telebot import types
from telebot.apihelper import ApiTelegramException

from bot_app import bot

list_to_check = [123, 32, 10644997]


@bot.message_handler(commands=['online_game'])
def start_new_online_game_session(message):
    bot.send_message(message.chat.id, '')


@bot.callback_query_handler(func=lambda call: True)
def qweqwe(call):
    bot.send_message(call.message.chat.id, call)


bot.send_message('7026124904', 'привет!')

bot.polling(none_stop=True)

ApiTelegramException


def get_linked_users(user_id)

def invite_friend(message):
