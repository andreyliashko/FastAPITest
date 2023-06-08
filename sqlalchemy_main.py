from typing import List
import uuid
import databases
import sqlalchemy
from fastapi import FastAPI

import config
import scremas

app = FastAPI()

DataBaseUrl = f'postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.db_name}'
data_base = databases.Database(DataBaseUrl)
metadata = sqlalchemy.MetaData()
table_name = "py_users"

users = sqlalchemy.Table(
    table_name,
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("create_at", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DataBaseUrl)
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await data_base.connect()


@app.on_event("shutdown")
async def shutdown():
    await data_base.disconnect()


@app.get('/users/us_id', response_model=scremas.UserList)
async def getUserById(us_id: str):
    query = users.select().where(users.c.id == us_id)
    return await data_base.fetch_one(query)


@app.get("/users", response_model=List[scremas.UserList])
async def find_all_users():
    query = users.select()
    return await data_base.fetch_all(query)


@app.post('/addUser')
async def addNewUser(user: scremas.AutoId):
    query = users.insert().values(
        id=str(uuid.uuid1()),
        username=user.username,
        password=user.password,
        first_name=user.first_name,
        last_name=user.password,
        create_at=user.create_at,
    )
    return await data_base.execute(query)
