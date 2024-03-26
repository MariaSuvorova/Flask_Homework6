from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from uvicorn import run
import router_users
import router_goods
import router_orders
from fake_data import fake_data

app = FastAPI()


@app.get('/db_data/', response_model=dict)
async def insert_fake_data_to_db():
    await fake_data()
    return {'message': 'fake DB ready for test'}


app.include_router(router_users.router)
app.include_router(router_goods.router)
app.include_router(router_orders.router)


@app.get("/", tags=["Redirect to Swagger"], response_class=RedirectResponse)
async def redirect_index():
    return "http://127.0.0.1:8000/docs"


if __name__ == "__main__":
    run("main:app", host="127.0.0.1", port=8000, reload=True)
