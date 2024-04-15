import sqlalchemy
from .db_session import SqlAlchemyBase
from .nutrition_program import NutritionProgram
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
import pickle


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    weight = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    best_sport_results = sqlalchemy.Column(sqlalchemy.PickleType, default=pickle.dumps({}), nullable=True)
    last_date_pfcc_controlled = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    nutrition_program_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("nutrition_programs.id"))
    nutrition_program = orm.relationship('NutritionProgram')
