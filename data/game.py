import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'game'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    rating = sqlalchemy.Column(sqlalchemy.Integer)
    #histories = relationship('History')
    dis_rating = sqlalchemy.Column(sqlalchemy.Integer)
