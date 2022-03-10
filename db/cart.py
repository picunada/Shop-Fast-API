import sqlalchemy
from .connect import metadata
from .item import items
import datetime

cart = sqlalchemy.Table(
    "cart",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False),
    # sqlalchemy.Column("items", sqlalchemy.ARRAY(sqlalchemy.Integer)),
    sqlalchemy.Column("items", sqlalchemy.JSON),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)