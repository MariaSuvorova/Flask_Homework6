from datetime import date
from decimal import Decimal
from random import choice, randint, uniform
from models import OrderStatus
from database import db, users, goods, orders


async def fake_data():
    USERS = 5
    GOODS = 20
    ORDERS = 5
    MIN, MAX = 1, 100_000

    for i in range(USERS):
        query = users.insert().values(firstname=f'Имя_{i}',
                                      lastname=f'Фамилия_{i}',
                                      email=f'почта{i}@test.ru',
                                      password=f'password{i}')
        await db.execute(query)

    for i in range(GOODS):
        query = goods.insert().values(
            title=f'Название{i}',
            description=f'Описание{i}',
            price=round(Decimal(uniform(MIN, MAX)), 2)
            )
        await db.execute(query)

    for i in range(ORDERS):
        query = orders.insert().values(user_id=randint(1, USERS),
                                       good_id=randint(1, GOODS),
                                       date=date.today(),
                                       status=choice(list(OrderStatus)))
        await db.execute(query)
