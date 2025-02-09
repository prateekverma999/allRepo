from fastapi import status, HTTPException, Depends, APIRouter, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Database import database, model, schema, utils


routs = APIRouter(
    prefix="/users",
    tags=['Users']
)


@routs.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponce)
def create_users(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    try:
        # Hash the password - user.password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        # Create user
        new_user = model.User(**user.model_dump())  # Use model_dump() to convert Pydantic model to dictionary
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()  # Rollback to prevent broken transactions
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
    

@routs.get("/{id}", response_model=schema.UserResponce)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id:{id} not exist")
    return user