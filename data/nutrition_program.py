import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Nutrition_program(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'nutrition_programs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    short_description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    proteins = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    fats = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    carbohydrates = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    calories = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    default_nutrition_program = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)

    user_id = orm.relationship("User", back_populates='nutrition_program')