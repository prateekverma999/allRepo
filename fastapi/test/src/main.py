from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from random import randint
from sqlalchemy.orm import Session
from Database import model
from Database.database import get_db, engine

app = FastAPI()

model.base.metadata.create_all(bind=engine)

class Post(BaseModel):
    name: str
    age: int
    city: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/home")
def get_home():
    return {'message': 'Welcome to the API'}

@app.get("/sqlconnect")
def test_db(db: Session = Depends(get_db)):

    posts = db.query(model.Post).all()
    return {'message': posts}

@app.get('/posts')
def get_post(db : Session = Depends(get_db)):
    post = db.query(model.Post).all()
    return {'post': post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session = Depends(get_db)):
    # new_post = model.Post(name=post.name, age=post.age, city=post.city, published=post.published, rating=post.rating)
    new_post = model.Post(**post.model_dump()) # Using model_dump() instead of dict()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'post': new_post}

@app.get("/posts/recent")
def get_recent_posts():
    cursor.execute(""" SELECT * FROM \"myPost\" 
                   ORDER BY id 
                   DESC 
                   LIMIT 3 """)
    post = cursor.fetchall()
    return {'post': post}

@app.get("/posts/{id}")
def get_post_by_id(id: int, response: Response):
    cursor.execute(""" SELECT * FROM \"myPost\" 
                   WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")

    return {'post': post}

@app.delete("/posts/{id}", status_code=status.HTTP_410_GONE )
def delete_post(id: int):
    cursor.execute(""" DELETE FROM \"myPost\" 
                   WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    conn.commit()
    return {'message': f"post with id: {id} has been deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE \"myPost\" SET name = %s, age = %s, city = %s, published = %s, rating = %s 
                   WHERE id = %s RETURNING * """,
                   (post.name, post.age, post.city, post.published, post.rating, str(id)))
    update_post = cursor.fetchone()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    conn.commit()
    return {'message': f"post with id: {id} has been updated"}

@app.patch("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE \"myPost\" SET name = %s, age = %s, city = %s, published = %s, rating = %s 
                   WHERE id = %s RETURNING * """,
                   (post.name, post.age, post.city, post.published, post.rating, str(id)))
    update_post = cursor.fetchone()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    conn.commit()
    return {'message': f"post with id: {id} has been updated"}
