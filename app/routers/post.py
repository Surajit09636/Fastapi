from .. import models, Schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/")
def get_post(db: Session = Depends(get_db), response_model=list[Schemas.Post]):
    # cursor.execute(""" SELECT * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.Post)
def create_post(post: Schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO POSTS (title, content, published) VALUES(%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post =models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), response_model=Schemas.Post):
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

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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



@router.put("/{id}")
def update_post(id: int, post: Schemas.CreatePost, db: Session = Depends(get_db), response_model=Schemas.Post):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()