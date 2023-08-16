from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import session
from sqlalchemy.sql.functions import mode
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth


# The code that creates tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --------------------------------------------------------------------------

# 43-44 Database
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connection to the database was successful.')
        break
    except Exception as error:
        print(f'Connection to the database failed.\nError: {error}')
        time.sleep(2)
# --------------------------------------------------------------------------

# Related to part 21 - find a special post by id
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# Related to part 24 - find a special post-index by id
def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i
# -------------------------------------------------------------------------

# 18 Storing Posts in Array
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like Pizza", "id": 2}]


# ------------------------------------------------*****************----------------------------------------------------
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# ------------------------------------------------*****************----------------------------------------------------

@app.get("/")
def root():
    return {"message": "Welcome to my API!!!!"}


























