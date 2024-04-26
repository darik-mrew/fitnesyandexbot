import sqlalchemy
from .db_session import SqlAlchemyBase
from .nutrition_program import NutritionProgram
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
import pickle


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    weight = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    best_sport_results = sqlalchemy.Column(sqlalchemy.PickleType, default=pickle.dumps({}), nullable=True)
    last_date_cpfc_controlled = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    current_cpfc = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True, default=pickle.dumps(None))
    sport = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    items = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    current_nutrition_program_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("nutrition_programs.id"))
    current_nutrition_program = orm.relationship('NutritionProgram')

    all_nutrition_programs_id = sqlalchemy.Column(sqlalchemy.PickleType, nullable=True, default=pickle.dumps([]))
