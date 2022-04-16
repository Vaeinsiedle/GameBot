import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class History(SqlAlchemyBase):
    __tablename__ = 'history'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    user = relationship('User', back_populates='histories')
    game_id = sqlalchemy.Column(sqlalchemy.Integer)
    game = relationship('Game', back_populates='games')
    result = sqlalchemy.Column(sqlalchemy.Integer)
