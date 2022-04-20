import datetime
import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_discord = sqlalchemy.Column(sqlalchemy.String)
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=1000)
    #histories = relationship('History')
    give_coin = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)