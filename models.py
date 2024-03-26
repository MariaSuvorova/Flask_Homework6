from decimal import Decimal
from datetime import date
from enum import StrEnum
from pydantic import BaseModel, Field, EmailStr


class UserIn(BaseModel):
    firstname: str = Field(title="Имя пользователя", min_length=3,
                           max_length=50)
    lastname: str = Field(title="Фамилия пользователя", min_length=3,
                          max_length=50)
    email: EmailStr = Field(title="Адрес эл. почты", max_length=128)
    password: str = Field(title="Пароль", min_length=8, max_length=128)


class User(BaseModel):
    id: int
    firstname: str = Field(title="Имя пользователя", min_length=3,
                           max_length=50)
    lastname: str = Field(title="Фамилия пользователя", min_length=3,
                          max_length=50)
    email: EmailStr = Field(title="Адрес эл. почты", max_length=128)
    password: str


class GoodIn(BaseModel):
    title: str = Field(title="Название товара", min_length=3, max_length=128)
    description: str = Field(title="Описание товара", min_length=3,
                             max_length=1024)
    price: Decimal = Field(title="Цена товара", gt=0, le=100_000, prec=2)


class Good(GoodIn):
    id: int
    title: str = Field(title="Название товара", min_length=3, max_length=128)


class OrderStatus(StrEnum):
    NEW = 'новый'
    PAY_AWAIT = 'ожидает оплаты'
    PAY_RECEIVED = 'оплачен'
    CONFIRMED = 'подтвержден'
    READY_TO_SHIP = 'подготовлен к отгрузке'
    SHIPPED = 'в пути'
    READY_TO_RECEIVE = 'готов к получению'
    RECEIVED = 'получен'
    CANCELED = 'отменен'
    EXPIRED = 'истекший'


class OrderIn(BaseModel, use_enum_values=True):
    user_id: int = Field()
    good_id: int = Field()
    date: date
    status: OrderStatus


class Order(OrderIn):
    id: int
