from fastapi import status, HTTPException, APIRouter, Depends, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import utils, schemas, models

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends((get_db))):


    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    
    # Error handling for duplicate emails missing
    db.add(new_user) 

    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with id {id} does not exist")
    return user_query.first()