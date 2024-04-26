import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class NutritionProgram(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'nutrition_programs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    short_description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    proteins = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    fats = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    carbohydrates = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    calories = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    default_nutrition_program = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    users = orm.relationship("User", back_populates='current_nutrition_program')

    def __repr__(self):
        return (f'{self.id}. {self.title}\nКБЖУ на кг веса.\nКалории в день: {self.calories} г.\nБелки в день: '
                f'{self.proteins} г.\nЖиры в день: {self.fats} г.\nУглеводы: {self.carbohydrates}\nОписание: '
                f'{self.short_description}')
