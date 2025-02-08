from fastapi import FastAPI, status, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from Database import database, model, schema

app = FastAPI()

# Ensure database tables are created
model.Base.metadata.create_all(bind=database.engine)


@app.get("/home")
def get_home():
    return {'message': 'Welcome to the API'}


# ✅ Filtering, Pagination, Sorting, and Search
@app.get('/posts', response_model=list[schema.PostResponce])
def get_posts(
    db: Session = Depends(database.get_db),
    name: Optional[str] = Query(None, description="Filter posts by name"),
    city: Optional[str] = Query(None, description="Filter posts by city"),
    published: Optional[bool] = Query(None, description="Filter by published status"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Limit the number of results"),
    offset: Optional[int] = Query(0, ge=0, description="Skip initial results"),
    order_by: Optional[str] = Query("id", description="Sort by a field (id, name, age, city, rating)"),
    order: Optional[str] = Query("asc", description="Sort order (asc or desc)")
):
    query = db.query(model.Post)

    # Filtering
    if name:
        query = query.filter(model.Post.name.ilike(f"%{name}%"))  # Case-insensitive search
    if city:
        query = query.filter(model.Post.city.ilike(f"%{city}%"))
    if published is not None:
        query = query.filter(model.Post.published == published)

    # Sorting
    if hasattr(model.Post, order_by):
        if order.lower() == "desc":
            query = query.order_by(desc(getattr(model.Post, order_by)))
        else:
            query = query.order_by(asc(getattr(model.Post, order_by)))

    # Pagination
    posts = query.offset(offset).limit(limit).all()
    
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponce)
def create_post(post: schema.PostCreate, db: Session = Depends(database.get_db)):
    new_post = model.Post(**post.model_dump())  # Use model_dump() to convert Pydantic model to dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/recent", response_model=list[schema.PostResponce])
def get_recent_posts(db: Session = Depends(database.get_db)):
    post = db.query(model.Post).order_by(model.Post.id.desc()).limit(3).all()
    return post

@app.get("/posts/{id}", response_model=schema.PostResponce)
def get_post_by_id(id: int, db: Session = Depends(database.get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_410_GONE)
def delete_post(id: int, db: Session = Depends(database.get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message': f"Post with id: {id} has been deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(database.get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {'message': f"Post with id: {id} has been fully updated"}

@app.patch("/posts/{id}")
def partial_update_post(id: int, post: schema.PostUpdate, db: Session = Depends(database.get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} not found")

    updated_data = {k: v for k, v in post.model_dump().items() if v is not None}
    if updated_data:
        post_query.update(updated_data, synchronize_session=False)
        db.commit()

    return {'message': f"Post with id: {id} has been partially updated"}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponce)
def users(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    new_user = model.User(**user.model_dump())  # Use model_dump() to convert Pydantic model to dictionary
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user