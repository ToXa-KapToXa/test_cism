import sqlalchemy
from .db_session import SqlAlchemyBase


class RegularTable(SqlAlchemyBase):
    __tablename__ = 'regular'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    marker = sqlalchemy.Column(sqlalchemy.Text)
    regular_expression = sqlalchemy.Column(sqlalchemy.Text)
    version = sqlalchemy.Column(sqlalchemy.Text)