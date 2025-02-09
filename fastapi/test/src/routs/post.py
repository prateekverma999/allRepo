from fastapi import status, HTTPException, Depends, Query, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from Database import database, model, schema, utils

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schema.PostResponce])
def get_posts(
    db: Session = Depends(database.get_db),
    title: Optional[str] = Query(None, description="Filter posts by title"),
    content: Optional[str] = Query(None, description="Filter posts by content"),
    published: Optional[bool] = Query(None, description="Filter by published status"),
    limit: int = Query(10, ge=1, le=100, description="Limit results"),
    offset: int = Query(0, ge=0, description="Skip initial results"),
    order_by: str = Query("id", description="Sort by field"),
    order: str = Query("asc", description="Sort order"),
):
    query = utils.apply_filters(db.query(model.Post), title, content, published)
    if hasattr(model.Post, order_by):
        query = query.order_by(desc(getattr(model.Post, order_by)) if order == "desc" else asc(getattr(model.Post, order_by)))
    return query.offset(offset).limit(limit).all()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponce)
def create_post(post: schema.PostCreate, db: Session = Depends(database.get_db)):
    new_post = model.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/recent", response_model=List[schema.PostResponce])
def get_recent_posts(db: Session = Depends(database.get_db)):
    return db.query(model.Post).order_by(model.Post.id.desc()).limit(3).all()

@router.get("/{id}", response_model=schema.PostResponce)
def get_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_410_GONE)
def delete_post(id: int, db: Session = Depends(database.get_db)):
    if db.query(model.Post).filter(model.Post.id == id).delete(synchronize_session=False):
        db.commit()
        return {"message": f"Post with id: {id} has been deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

@router.put("/{id}")
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(database.get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message": f"Post with id: {id} has been updated"}

@router.patch("/{id}")
def partial_update_post(id: int, post: schema.PostUpdate, db: Session = Depends(database.get_db)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    updated_data = {k: v for k, v in post.model_dump().items() if v is not None}
    if updated_data:
        post_query.update(updated_data, synchronize_session=False)
        db.commit()
    return {"message": f"Post with id: {id} has been partially updated"}
