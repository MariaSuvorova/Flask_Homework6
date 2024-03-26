from fastapi import HTTPException
from enum import Enum

from database import db, users, goods, orders


class DBTables(Enum):
    users = 'users'
    items = 'goods'
    orders = 'orders'


async def id_check(id: int, db_table_name: DBTables):
    if_id_exist = globals()[f'_{db_table_name}_id_check']
    await if_id_exist(id)


async def _users_id_check(id: int) -> None:
    if len(await db.fetch_all(query=users.select().where(users.c.id == id))) == 0:
        raise HTTPException(status_code=422, 
                            detail=f'Пользователя с id={id} не существует')


async def _goods_id_check(id: int) -> None:
    if len(await db.fetch_all(query=goods.select().where(goods.c.id == id))) == 0:
        raise HTTPException(status_code=422, 
                            detail=f'Товара с id={id} не существует')


async def _orders_id_check(id: int) -> None:
    if len(await db.fetch_all(query=orders.select().where(orders.c.id == id))) == 0:
        raise HTTPException(status_code=422, 
                            detail=f'Заказа с id={id} не существует')
