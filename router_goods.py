from fastapi import APIRouter
from id_check import id_check
from models import GoodIn, Good
from database import db, goods

router = APIRouter(prefix="/goods", tags=["Goods"])


@router.post("/", response_model=Good)
async def create_good(good_in: GoodIn):
    query = goods.insert().values(**good_in.model_dump())
    last_record_id = await db.execute(query)
    return {**good_in.model_dump(), "id": last_record_id}


@router.get("/", response_model=list[Good])
async def read_all_goods():
    '''Read all goods'''
    query = goods.select()
    return await db.fetch_all(query)


@router.get("/{good_id}", response_model=Good)
async def read_good_by_id(good_id: int):
    '''Read good by id'''
    await id_check(good_id, goods)
    query = goods.select().where(goods.c.id == good_id)
    return await db.fetch_one(query)


@router.put("/{good_id}", response_model=Good)
async def update_good(good_id: int, good_in: GoodIn):
    await id_check(good_id, goods)
    query = goods.update().where(goods.c.id == good_id).values(**good_in.model_dump())
    await db.execute(query)
    return {**good_in.model_dump(), "id": good_id}


@router.delete("/{good_id}", response_model=dict)
async def delete_good(good_id: int):
    await id_check(good_id, goods)
    query = goods.delete().where(goods.c.id == good_id)
    await db.execute(query)
    return {"message": "Good deleted"}
