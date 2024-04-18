import telebot
from telebot import types
from dotenv import load_dotenv
from data import db_session
from data.user import User
import os
import pickle


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


def create_user(user_id):
    user = User()
    user.id = user_id
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def add_helper_to_message(text):
    text += '\n\nОтправте сообщение /commands или /команды, чтобы увидеть список всех возможных команд бота!'
    return text


@bot.message_handler(commands=['start', 'старт'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Начнем!")
    markup.add(button)

    user_name = message.from_user.username
    bot.send_message(message.chat.id,
                     f'Приветствую тебя, {user_name}! Я бот, созданный, чтобы помочь тебе в спорте. Начнем?',
                     reply_markup=markup)


# не забывать добавлять сюда новые команды
@bot.message_handler(commands=['команды', 'commands'])
def send_commands(message):
    possible_commands = {'/commands или /команды': 'выводит список список всех команд бота.'}

    text = '\n'.join([f'{key} - {possible_commands[key]}' for key in possible_commands.keys()])
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['sport_results', 'спортивные результаты'])
def send_all_sport_results(message):
    db_sess = db_session.create_session()

    user_id = int(message.chat.id)
    user = db_sess.query(User).filter(User.id == user_id).one()

    sport_results = pickle.loads(user.best_sport_results)
    if len(sport_results.keys()) == 0:
        text = 'У вас пока что не записаны никакие спортивные результаты!'
    else:
        text = '\n'.join([f'{exercise}: {sport_results[exercise]}' for exercise in sport_results.keys()])

    bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['write_result', 'записать результат'])
def write_sport_result(message):
    print(dir(message.date))
    print(message.date.real)
    print(message.date.conjugate)
    print(message.date.from_bytes)
    print(message.date.to_bytes)

    print(message.date)
    print(message.text)


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
        bot.reply_to(message, add_helper_to_message(text), reply_markup=markup)


# добавить функцию add_helper_to_message при необходимости
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет, нужна помощь?")


db_session.global_init("db/data_base.db")
bot.polling()
