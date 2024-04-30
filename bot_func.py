import telebot
from telebot import types
from dotenv import load_dotenv
from data import db_session
from data.user import User
from data.nutrition_program import NutritionProgram
import os
import pickle
import sqlalchemy
import datetime
import logging
import working_with_maps


logging.basicConfig(filename='log/bot_log.log', format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                    level=logging.ERROR)
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


def create_user(user_id):
    user = User()
    user.id = user_id
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def create_nutrition_program(user_id, title, short_description, cpfc):
    nutrition_program = NutritionProgram()
    nutrition_program.default_nutrition_program = False
    nutrition_program.title = title
    nutrition_program.short_description = short_description
    nutrition_program.calories = cpfc[0]
    nutrition_program.proteins = cpfc[1]
    nutrition_program.fats = cpfc[2]
    nutrition_program.carbohydrates = cpfc[3]

    db_sess = db_session.create_session()
    db_sess.add(nutrition_program)

    user = db_sess.query(User).filter(User.id == int(user_id)).one()
    all_nutrition_programs_id = pickle.loads(user.all_nutrition_programs_id)
    all_nutrition_programs_id.append(nutrition_program.id)
    user.all_nutrition_programs_id = pickle.dumps(all_nutrition_programs_id)

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


@bot.message_handler(commands=['команды', 'commands'])
def send_commands(message):
    possible_commands = {'/commands или /команды': 'выводит список список всех команд бота.',
                         '/sh_sp_res или /спортивные результаты':
                             'выводит список всех ваших спортивных результатов',
                         '/wr_sp_res или /записать результат':
                             'записывает ваш спортивный результат.\nФормат сообщения: '
                             '<сама команда> Название: <название упражнения> Резульат: <ваш резульат>.\n'
                             'Пример: /write_result Название: Жим лежа Результат: 100 кг.'
                             ' Важно соблюдение формата, иначе результат не запишется или запишется неправильно!',
                         '/del_sp_res или /удалить результат':
                             'удаляет один записанный спортивный результат.\nФормат сообщения: <сама команда>'
                             ' <название упражнения>.\nПример: /delete_result Жим лежа.',
                         '/del_all_sp_res или /удалить все результаты':
                             'удаляет все ваши спортивные результаты из списка.',
                         '/wr_cpfc или /записать кбжу':
                             'записасть потребленное кбжу.\nФормат сообщения: <сама команда> <калории, '
                             'белки, жиры, углеводы>\nПример: /wr_cpfc 500, 20, 20, 20',
                         '/sh_cur_cpfc или /показать текущее кбжу':
                             'показывает потребленное в течении дня кбжу.',
                         '/add_my_nut_pr или /добавить свою программу питания':
                             'добавляет вашу программу питания в список всех программ и в общую базу данных.'
                             ' Кбжу указывается на кг веса\nФормат сообщения: <сама команда> название: '
                             '<название программы питания> кбжу: <калории>, <белки>, <жиры>, <углеводы> описание: '
                             '<краткое описание вашей программы>.\nПример /add_my_nut_pr название: моё крутое название '
                             'кбжу: 50, 2, 1, 3 описание: моё крутое описание',
                         '/del_nut_pr или /удалить программу питания':
                             'удаляет программу питания из вашего списка програм.\nФормат сообщения: <сама команда>'
                             ' <id программы питания>.\nПример: /del_nut_pr 23',
                         '/chs_nut_pr или /выбрать программу питания':
                             'устанавливает программу питания из вашего списка программ как текущую(необходимо для '
                             'контроля потребленного кбжу).\nФормат сообщения: <сама команда> <id программы '
                             'питания>.\nПример: /chs_nut_pr 1',
                         '/add_nut_pr_id или /добавить программу питания по id':
                             'добавляет программу питания из общей базы, созданной пользователями, по id, если такая'
                             ' существует.\nФормат сообщения: <сама команда> <id программы из базы>. '
                             '\nПример: /add_nut_pr_id 45',
                         '/set_weight или /установить вес':
                             'сохраняет ваш вес, необходимо для контроля потребленного кбжу.\nФормат сообщения: '
                             '<сама команда> <ваш вес>.\nПример: /set_weight 75',
                         '/sh_nut_prs или /показать программы питания':
                             'показывает список ваших программ питания(номер программы в списке - её id в '
                             'безе данных).',
                         '/sh_cur_nut_pr или /показать текущую программу питания':
                             'показывает выбранную вами программу питания.',
                         '/nearby_gyms или /спортзалы рядом':
                             'отправляет карту с вашим местоположением и местоположением нескольких ближайших к вам'
                             ' спортзалов(чем точнее вы укажете свой адрес, тем точнее составится карта).'
                             '\nФормат сообщения: <сама команда><ваш адрес>\nПример: /nearby_gyms город'
                             ' Лиски, улица Коминтерна, дом 104.'}

    text = '\n\n'.join([f'{key} - {possible_commands[key]}' for key in possible_commands.keys()])
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['nearby_gyms', 'спортзалы рядом'])
def send_map(message):
    try:
        user_address = message.text.replace('/nearby_gyms', '').replace('/спортзалы рядом', '').strip()
        user_latitude, user_longitude = working_with_maps.get_coordinates(user_address)
        gyms = working_with_maps.get_nearby_gyms(user_latitude, user_longitude)

        map = working_with_maps.draw_map(user_latitude, user_longitude, gyms)
        text = 'Красная метка - ваше местоположение, синие - местоположения спортзалов.'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')

        map = open('data/сильный котик.png', 'rb').read()
        text = ('Возникла неизвестная оошибка или вы указали некорректный адрес,'
                ' приносим свои извиненения.\nПосмотрите пока на этого сильного и крутого котика!')
    finally:
        bot.send_photo(message.chat.id, map)
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['sh_sp_res', 'спортивные результаты'])
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


@bot.message_handler(commands=['wr_sp_res', 'записать результат'])
def write_sport_result(message):
    try:
        user_input = message.text.replace(
            ('/wr_sp_res' if '/wr_sp_res' in message.text.lower() else '/записать результат'), '').strip().lower()
        user_input = user_input.replace('название:', '~~~~')
        user_input = user_input.replace('результат:', '~~~~')
        user_input = [i.strip() for i in user_input.split('~~~~') if i != '']
        title, result = user_input[0].capitalize(), user_input[1].capitalize()

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()

        sport_results = pickle.loads(user.best_sport_results)
        sport_results[title] = result

        user.best_sport_results = pickle.dumps(sport_results)
        db_sess.commit()

        text = 'Результат записан!'
    except IndexError:
        text = 'Неправильный формат ввода!'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')
        text = 'Возникла неизвестная ошибка, приносим свои извинения.'
    finally:
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['del_sp_res', 'удалить результат'])
def delete_sport_result(message):
    title = (message.text.replace(
        ('/del_sp_res' if '/del_sp_res' in message.text.lower() else '/удалить результат'), '').strip().lower()
                  .capitalize())

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
    sport_results = pickle.loads(user.best_sport_results)

    if title in sport_results.keys():
        del sport_results[title]
        user.best_sport_results = pickle.dumps(sport_results)
        db_sess.commit()

        text = f'Запись об упражнении "{title}" успешно удалена!'
    else:
        text = f'Упражнение "{title}" не найдено, проверьте коррекность входных данных.'

    bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['del_all_sp_res', 'удалить все результаты'])
def delete_all_sport_results(message):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
    user.best_sport_results = pickle.dumps({})
    db_sess.commit()

    text = 'Записи о всех спортивных результатах успешно удалены!'
    bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['wr_cpfc', 'записать кбжу'])
def write_cpfc(message):
    try:
        cpfc = (message.text.replace('/wr_cpfc', '').replace('/записать кбжу', '').replace(', ', ',').strip().
                split(','))

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
        nutrition_porgram = user.current_nutrition_program

        text = ''
        if user.weight is None or user.current_nutrition_program is None:
            text = 'У вас не определен вес или программа питания, вы пока не можете записывать потребленное кбжу.'
        else:
            current_cpfc = pickle.loads(user.current_cpfc)
            if user.last_date_cpfc_controlled is None or pickle.loads(user.current_cpfc) is None:
                current_cpfc = [0, 0, 0, 0]
            elif user.last_date_cpfc_controlled != datetime.date.today():
                text = (f'Ваше потребленное кбжу за прошлый день: '
                        f'{current_cpfc[0]}/{int(nutrition_porgram.calories * user.weight)}, '
                        f'{current_cpfc[1]}/{int(nutrition_porgram.proteins * user.weight)}, '
                        f'{current_cpfc[2]}/{int(nutrition_porgram.fats * user.weight)}, '
                        f'{current_cpfc[3]}/{int(nutrition_porgram.carbohydrates * user.weight)}.\n')
                current_cpfc = [0, 0, 0, 0]

            for i in range(0, 4):
                current_cpfc[i] += float(cpfc[i])

            user.current_cpfc = pickle.dumps(current_cpfc)
            user.last_date_cpfc_controlled = datetime.date.today()
            db_sess.commit()

            text += 'Потребленное кбжу записано.'
    except ValueError or IndexError:
        text = 'Неправильный формат ввода!'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')
        text = 'Возникла неизвестная оошибка, приносим свои извиненения.'
    finally:
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['sh_cur_cpfc', 'показать текущее кбжу'])
def show_current_cpfc(message):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
    current_cpfc = pickle.loads(user.current_cpfc)
    nutrition_porgram = user.current_nutrition_program

    if user.last_date_cpfc_controlled is None:
        text = 'Вы еще ни разу не записывали потребленное кбжу.'
    elif datetime.date.today() != user.last_date_cpfc_controlled:
        user.current_cpfc = pickle.dumps([0, 0, 0, 0])
        user.last_date_cpfc_controlled = datetime.date.today()
        db_sess.commit()

        text = (f'Ваше потребленное кбжу за прошлый день: '
                f'{current_cpfc[0]}/{int(nutrition_porgram.calories * user.weight)}, '
                f'{current_cpfc[1]}/{int(nutrition_porgram.proteins * user.weight)}, '
                f'{current_cpfc[2]}/{int(nutrition_porgram.fats * user.weight)}, '
                f'{current_cpfc[3]}/{int(nutrition_porgram.carbohydrates * user.weight)}.'
                f'\nВаше текущее потребленное кбжу: '
                f'0/{int(nutrition_porgram.calories * user.weight)}, 0/{int(nutrition_porgram.proteins * user.weight)},'
                f' 0/{int(nutrition_porgram.fats * user.weight)},'
                f' 0/{int(nutrition_porgram.carbohydrates * user.weight)}.')
    else:
        user.last_date_cpfc_controlled = datetime.date.today()
        db_sess.commit()

        text = (f'Ваше текущее потребленное кбжу: {current_cpfc[0]}/{int(nutrition_porgram.calories * user.weight)}, '
                f'{current_cpfc[1]}/{int(nutrition_porgram.proteins * user.weight)}, '
                f'{current_cpfc[2]}/{int(nutrition_porgram.fats * user.weight)}, '
                f'{current_cpfc[3]}/{int(nutrition_porgram.carbohydrates * user.weight)}.')

    bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['добавить свою программу питания', 'add_my_nut_pr'])
def add_my_nutrition_program(message):
    try:
        user_input = message.text.replace(('/add_my_nut_pr' if '/add_my_nut_pr' in
                                                               message.text.lower() else
                                           '/добавить свою программу питания'), '').strip().lower()
        user_input = user_input.replace('название:', '~~~~').replace('кбжу:', '~~~~').replace('описание:', '~~~~')
        title, cpfc, short_description = [i.capitalize().strip() for i in user_input.split('~~~~') if i != '']
        cpfc = [float(i) for i in cpfc.replace(', ', ',').split(',')]
        create_nutrition_program(message.chat.id, title, short_description, cpfc)

        text = f'Программа {title} успешно добавлена!'
    except IndexError:
        text = 'Неправильный формат ввода!'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')
        text = 'Возникла неизвестная ошибка, приносим свои извинения.'
    finally:
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['удалить программу питания', 'del_nut_pr'])
def del_nutrition_program(message):
    try:
        nutrition_program_id = int(int(message.text.replace('/del_nut_pr', '')
                                       .replace('/удалить программу питания', '')))

        db_sess = db_session.create_session()
        nutrition_program = (db_sess.query(NutritionProgram).filter(NutritionProgram.id == int(nutrition_program_id)).
                             one())
        user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
        all_nutrition_programs_id = pickle.loads(user.all_nutrition_programs_id)
        if nutrition_program.default_nutrition_program:
            text = 'Это базовая программа питания, ее нельзя удалить!'
        elif nutrition_program_id not in all_nutrition_programs_id:
            text = f'У вас нет программы питания с id {nutrition_program_id}!'
        else:
            all_nutrition_programs_id.remove(nutrition_program_id)
            user.all_nutrition_programs_id = pickle.dumps(all_nutrition_programs_id)
            db_sess.commit()

            text = 'Программа питания удалена!'
    except ValueError:
        text = 'Неправильный формат ввода!'
    except sqlalchemy.exc.NoResultFound:
        text = 'Программы питания с таким id не существует!'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')
        text = 'Возникла неизвестная ошибка, приносим свои извинения.'
    finally:
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['chs_nut_pr', 'выбрать программу питания'])
def choose_nutrition_program(message):
    try:
        nutrition_program_id = int(message.text.replace('/chs_nut_pr', '')
                                   .replace('/выбрать программу питания', ''))

        db_sess = db_session.create_session()
        if nutrition_program_id in [i.id for i in db_sess.query(NutritionProgram).all()]:
            user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
            nutrition_program = db_sess.query(NutritionProgram).filter(NutritionProgram.id ==
                                                                       int(nutrition_program_id)).one()
            user.current_nutrition_program = nutrition_program
            db_sess.commit()

            text = 'Текущая программа питания выбрана!'
        else:
            text = 'Программы питания с таким id несуществует!'
    except ValueError:
        text = 'Неправильный формат ввода!'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')
        text = 'Возникла неизвестная ошибка, приносим свои извинения.'
    finally:
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['add_nut_pr_id', 'добавить программу питания по id'])
def add_nutrition_program_by_id(message):
    try:
        nutrition_program_id = int(message.text.replace('/add_nut_pr_id', '')
                                   .replace('/добавить программу питания по id', ''))

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
        all_nutrition_programs_id = pickle.loads(user.all_nutrition_programs_id)

        if nutrition_program_id in all_nutrition_programs_id:
            text = f'У вас уже сохранена программа питания с id {nutrition_program_id}!'
        elif nutrition_program_id in [i.id for i in db_sess.query(NutritionProgram).all()]:
            all_nutrition_programs_id.append(nutrition_program_id)
            user.all_nutrition_programs_id = pickle.dumps(all_nutrition_programs_id)
            db_sess.commit()

            text = 'Программа питания успешно добавлена!'
        else:
            text = 'Программы питания с таким id несуществует!'

    except ValueError:
        text = 'Неправильный формат ввода!'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')
        text = 'Возникла неизвестная ошибка, приносим свои извинения.'
    finally:
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['set_weight', 'установить вес'])
def set_weight(message):
    try:
        weight = float(message.text.replace('/set_weight', '').replace('/установить вес', '').strip())

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
        user.weight = weight
        db_sess.commit()

        text = 'Вес успешно установлен!'
    except ValueError:
        text = 'Неправильный формат ввода!'
    except Exception as e:
        logging.error(f'id:{message.chat.id} message:{message.text} type:{type(e)} error:{e}')
        text = 'Возникла неизвестная ошибка, приносим свои извинения.'
    finally:
        bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['sh_nut_prs', 'показать программы питания'])
def show_nutrition_programs(message):
    db_sess = db_session.create_session()
    default_nutrition_programs = db_sess.query(NutritionProgram).filter(NutritionProgram.default_nutrition_program
                                                                        == True).all()
    user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
    nutrition_porgams_id = pickle.loads(user.all_nutrition_programs_id)
    nutrition_porgams = [db_sess.query(NutritionProgram).filter(NutritionProgram.id == int(i)).one() for i in
                         nutrition_porgams_id]

    text = ('\n\n'.join([str(i) for i in default_nutrition_programs]) + '\n\n' +
            '\n\n'.join([str(i) for i in nutrition_porgams])).strip()
    bot.send_message(message.chat.id, add_helper_to_message(text))


@bot.message_handler(commands=['sh_cur_nut_pr', 'показать текущую программу питания'])
def show_current_nutrition_program(message):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(message.chat.id)).one()
    nutrition_program = user.current_nutrition_program

    text = str(nutrition_program)
    bot.send_message(message.chat.id, add_helper_to_message(text))


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


db_session.global_init("db/data_base.db")
bot.polling()
