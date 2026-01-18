from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()



class post(BaseModel):
    title: str
    content: str
    published: bool = True

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

@app.get("/")
async def root():
    return("mosi amigo")

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return{"data": posts}

@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return{"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:post, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO POSTS (title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post =models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return{"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     "SELECT * FROM posts WHERE id = %s",
    #     (id,)
    # )
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return {"post detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     "DELETE FROM posts WHERE id = %s RETURNING *",
    #     (id,)
    # )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_post(id: int, post: post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": "Successful"}

