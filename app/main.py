from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, Schemas, utils
from .database import SessionLocal, engine, get_db
from passlib.context import CryptContext
from .routers import post, user, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:  
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='suro1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected Successfully")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(5)
    
my_posts = [{"title": "Title of post 1", "content": "Content of post 1", "id": 1}, {
    "title": "Favourite games", "content": "I like Minecraft", "id": 2
}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return("mosi amigo")



