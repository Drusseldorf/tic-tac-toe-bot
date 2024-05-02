import telebot
from config.basic_config import settings

bot = telebot.TeleBot(settings.bot_settings.token)