from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Database import database, model, schema, utils

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponce)
def create_user(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    """Create a new user with hashed password. Returns the created user."""
    try:
        user.password = utils.hash(user.password)  # Hash password before storing
        db.add(new_user := model.User(**user.model_dump())) # ":-" walrus operator used to assign and return the value in one line
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()  # Ensure transaction rollback on error
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")

@router.get("/{id}", response_model=schema.UserResponce)
def get_user(id: int, db: Session = Depends(database.get_db)):
    """Retrieve a user by ID. Raises 404 if not found."""
    if not (user := db.query(model.User).filter(model.User.id == id).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not exist")
    return user