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
    text += '\n\nОтправьте сообщение /commands или /команды, чтобы увидеть список всех возможных команд бота!'
    return text


@bot.message_handler(commands=['start', 'старт'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tennis_button = types.KeyboardButton("Теннис")
    volleyball_button = types.KeyboardButton("Волейбол")
    basketball_button = types.KeyboardButton("Баскетбол")
    football_button = types.KeyboardButton("Футбол")
    fitness_button = types.KeyboardButton("Фитнес")
    swimming_button = types.KeyboardButton("Плавание")
    markup.add(tennis_button, volleyball_button, basketball_button, football_button, fitness_button, swimming_button)

    user_name = message.from_user.username
    bot.send_message(message.chat.id,
                     f'Приветствую тебя, {user_name}! Я бот, созданный, чтобы помочь тебе в спорте. '
                     f'Выбери вид спорта, который тебе интересен.',
                     reply_markup=markup)


@bot.message_handler(commands=['commands', 'команды'])
def send_commands(message):
    possible_commands = {'/commands или /команды': 'выводит список всех команд бота.'}

    text = '\n'.join([f'{key} - {possible_commands[key]}' for key in possible_commands.keys()])
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text in ['теннис', 'волейбол', 'баскетбол', 'футбол', 'фитнес', 'плавание'])
def handle_sport_buttons(message):
    chosen_sport = message.text
    if chosen_sport == 'теннис':
        bot.send_message(message.chat.id, 'Мячи для тенниса', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Купить", url="https://www.ozon.ru/category/tennisnye-myachi-11278/")))
    elif chosen_sport == 'волейбол':
        bot.send_message(message.chat.id, 'Мяч для волейбола', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Купить", url="https://www.ozon.ru/category/voleybolnye-myachi-11258/")))
    elif chosen_sport == 'баскетбол':
        bot.send_message(message.chat.id, 'Мяч для баскетбола', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Купить", url="https://www.ozon.ru/category/basketbolnye-myachi-11253/")))
    elif chosen_sport == 'футбол':
        bot.send_message(message.chat.id, 'Мяч для футбола', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Купить", url="https://www.ozon.ru/category/futbolnye-myachi-11277/")))
    elif chosen_sport == 'фитнес':
        bot.send_message(message.chat.id, 'Гантели для фитнеса', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Купить", url="https://www.ozon.ru/category/ganteli-11641/")))
    elif chosen_sport == 'плавание':
        bot.send_message(message.chat.id, 'Шапочки для плавания', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Купить", url="https://www.ozon.ru/category/shapochki-dlya-plavaniya-11184/")))


def add_sport_to_user_data(user_id, chosen_sport):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    user.chosen_sport = chosen_sport
    db_sess.commit()


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    chosen_sport = message.text
    add_sport_to_user_data(user_id, chosen_sport)


db_session.global_init("db/data_base.db")
bot.polling()
