# import os
from databases import Database
from sqlalchemy import MetaData, Table, Column, create_engine, ForeignKey, Date
from sqlalchemy import Integer, String, Enum, DECIMAL
from models import OrderStatus

# DB_URL = f"sqlite:///{os.path.relpath(os.getcwd(), '../')}.db"
DB_URL = "sqlite:///shop.db"
db = Database(DB_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('firstname', String(50), nullable=False),
    Column('lastname', String(50), nullable=False),
    Column('email', String(128), nullable=False),
    Column('password', String(128), nullable=False),
)

goods = Table(
    "goods",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(128), nullable=False),
    Column('description', String(1024), nullable=True),
    Column('price', DECIMAL, nullable=False),
)

orders = Table(
    "orders",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('good_id', ForeignKey('goods.id'), nullable=False),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('date', Date, nullable=False),
    Column('status', Enum(OrderStatus), nullable=False),
)


engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)
