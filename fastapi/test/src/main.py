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



# while True:
#     try:
#         conn = psycopg2.connect(host='172.31.248.137',
#                                 database='fastapi_1', 
#                                 user='postgres',
#                                 password='admin', 
#                                 cursor_factory=RealDictCursor
#                                 )
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)



@app.get("/home")
def get_home():
    return {'message': 'Welcome to the API'}

@app.get("/sqlconnect")
def test_db(db: Session = Depends(get_db)):
    return {'message': 'Successfully connected to database'}

@app.get('/posts')
def get_post():
    cursor.execute(""" SELECT * FROM \"myPost\" """)
    post = cursor.fetchall()
    return {'post': post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute(""" INSERT INTO \"myPost\" (name, age, city, published, rating) 
                   VALUES (%s, %s, %s, %s, %s) RETURNING *""",
                   (post.name, post.age, post.city, post.published, post.rating)
                   )
    new_post = cursor.fetchone()
    conn.commit()
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
