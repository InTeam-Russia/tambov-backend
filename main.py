from typing import Annotated

from fastapi import FastAPI, Depends

from auth.auth import oauth2_scheme
from auth.db import connect_to_db, close_all_connections
from auth.routes import router
from routes.routes import task_routers

app = FastAPI()
app.include_router(router)
app.include_router(task_routers)


@app.on_event("startup")
async def startup():
    await connect_to_db()


@app.on_event("shutdown")
async def shutdown():
    await close_all_connections()