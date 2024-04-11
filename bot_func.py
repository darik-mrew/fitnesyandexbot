import telebot
from dotenv import load_dotenv
import os


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.username
    bot.send_message(message.chat.id, f'Приветствую тебя, {user_id}! Я бот, созданный, чтобы помочь тебе в спорте. Начнем?')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет, нужна помощь?")


bot.polling()