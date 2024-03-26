from fastapi import APIRouter
from id_check import id_check
from models import UserIn, User
from database import db, users

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User)
async def create_user(user_in: UserIn):
    query = users.insert().values(**user_in.dict())
    last_record_id = await db.execute(query)
    return {**user_in.model_dump(), "id": last_record_id}


@router.get("/", response_model=list[User])
async def read_all_users():
    '''Read all users'''
    query = users.select()
    return await db.fetch_all(query)


@router.get("/{user_id}", response_model=User)
async def read_user_by_id(user_id: int):
    '''Read user by id'''
    await id_check(user_id, users)
    query = users.select().where(users.c.id == user_id)
    return await db.fetch_one(query)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_in: UserIn):
    await id_check(user_id, users)
    query = users.update().where(users.c.id == user_id).values(**user_in.model_dump())
    await db.execute(query)
    return {**user_in.model_dump(), "id": user_id}


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    await id_check(user_id, users)
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {"message": "User deleted"}
