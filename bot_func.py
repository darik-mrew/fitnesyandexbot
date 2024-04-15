import telebot
from telebot import types
from dotenv import load_dotenv
from data import db_session
from data.user import User
import os


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


def create_user(user_id):
    user = User()
    user.id = user_id
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Начнем!")
    markup.add(button)

    user_name = message.from_user.username
    bot.send_message(message.chat.id,
                     f'Приветствую тебя, {user_name}! Я бот, созданный, чтобы помочь тебе в спорте. Начнем?',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_button_click(message):
    if message.text == "Начнем!":
        user_id = message.chat.id
        db_sess = db_session.create_session()
        if user_id in [user.id for user in db_sess.query(User).all()]:
            text = "Вы уже зарегистрированы в системе!"
        else:
            create_user(user_id)
            text = "Вы успешно зарегистрированы в системе!"

        markup = types.ReplyKeyboardRemove()
        bot.reply_to(message, text, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет, нужна помощь?")


db_session.global_init("db/data_base.db")
bot.polling()
