from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Database import database, model, schema, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponce)
def create_user(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    """Create a new user with a hashed password."""
    try:
        user.password = utils.hash(user.password)  # Hash password before storing
        new_user = model.User(**user.model_dump())  # Convert Pydantic model to dictionary
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()  # Rollback transaction on error
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")

@router.get("/{id}", response_model=schema.UserResponce)
def get_user(id: int, db: Session = Depends(database.get_db)):
    """Retrieve a user by ID. Raises 404 if not found."""
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user
