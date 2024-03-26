from fastapi import APIRouter
from models import OrderIn, Order
from database import db, users, goods, orders
from id_check import id_check

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=Order)
async def create_order(order_in: OrderIn):
    await id_check(order_in.user_id, users)
    await id_check(order_in.good_id, goods)
    query = orders.insert().values(**order_in.dict())
    last_record_id = await db.execute(query)
    return {**order_in.model_dump(), "id": last_record_id}


@router.get("/", response_model=list[Order])
async def read_all_orders():
    '''Read all orders'''
    query = orders.select()
    return await db.fetch_all(query)


@router.get("/{order_id}", response_model=Order)
async def read_order_by_id(order_id: int):
    '''Read order by id'''
    await id_check(order_id, orders)
    query = orders.select().where(orders.c.id == order_id)
    return await db.fetch_one(query)


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order_in: OrderIn):
    await id_check(order_id, orders)
    query = orders.update().where(orders.c.id ==
                                  order_id).values(**order_in.model_dump())
    await db.execute(query)
    return {**order_in.model_dump(), "id": order_id}


@router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: int):
    await id_check(order_id, orders)
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {"message": "Order deleted"}
