import uvicorn
from fastapi import FastAPI

from routes import users, items, cart, auth
from db.connect import database


app = FastAPI(title="Shop API")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
