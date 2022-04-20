import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'countries'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    country = sqlalchemy.Column(sqlalchemy.String)
    capital = sqlalchemy.Column(sqlalchemy.String)
    flag = sqlalchemy.Column(sqlalchemy.String)
