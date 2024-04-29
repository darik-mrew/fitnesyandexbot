from data.nutrition_program import NutritionProgram
from data import db_session

db_session.global_init("db/data_base.db")

titles = ['Набор мышечной массы', 'Сушка', 'Удержание массы']
descriptions = ['Универсальное соотношение БЖУ в период набора мышечной массы – это до 20% жиров, порядка 30% белков и '
                'до 60% углеводов. При этом жиры – полиненасыщенные, углеводы – сложные. Минимум 3 приема пищи, '
                'потребление углеводов относительно тренировок – за 1.5-2 часа до и после.',
                'Составлять рацион на период сушки нужно индивидуально, исходя из ваших целей, физических особенностей '
                'и пищевых предпочтений. Пример соотношения БЖУ в период сушки – 35% белков, 20% жиров, 45% углеводов.',
                'Если ваша цель – правильное питание и удержание веса, то соотношение б/ж/у должно соответствовать '
                'формуле 30/30/40, т. е. 40% суточного рациона – углеводы, 30% — белки и 30% — жиры. Если цель '
                'похудеть, ваша формула 25/25/50 или 30/20/50.']
cpfc = [(45, 2, 1, 6), (25, 2.5, 1, 3), (35, 1.8, 1, 4)]

db_sess = db_session.create_session()

for title, short_description, cpfc in zip(titles, descriptions, cpfc):
    nutrition_program = NutritionProgram()
    nutrition_program.default_nutrition_program = True
    nutrition_program.title = title
    nutrition_program.short_description = short_description
    nutrition_program.calories = cpfc[0]
    nutrition_program.proteins = cpfc[1]
    nutrition_program.fats = cpfc[2]
    nutrition_program.carbohydrates = cpfc[3]

    db_sess.add(nutrition_program)

db_sess.commit()
