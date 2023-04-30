from fastapi import status, HTTPException, APIRouter, Depends, Response
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import utils, schemas, models, oauth2, token_utils, mailer_utils

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends((get_db))):


    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    
    # Error handling for duplicate emails missing
    try:
        db.add(new_user)

        token = token_utils.token(user.email)
        
        print(token)
        
        frontend_url = 'http://localhost:5173/'

        email_verification_endpoint = f'{frontend_url}confirm-email/{token}/'
        
        mail_body = {
            'email':user.email,
            'project_name': 'Room Booking App',
            'url': email_verification_endpoint
        }

        db.commit()

        mail_status = await mailer_utils.send_email_async(
            subject="Email Verification: Registration Confirmation",
            email_to=user.email, body=mail_body,
            template='template.html')
        
       
        db.refresh(new_user)

    except IntegrityError:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail = f"{user.email} is already registered!")
    else:
        return new_user    

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(models.User.id == id)

    if current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only Admins can view users")

    if user_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with id {id} does not exist")
    return user_query.first()

@router.get("/", response_model= List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    if current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only Admins can view users")
    
    user_query = db.query(models.User).all()

    return user_query
    
@router.get("self", response_model= schemas.UserOut)
def get_user(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    return current_user


@router.patch("self",  response_model = schemas.UserOut)
def update_user(newSelf: schemas.UserModify, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    
    try:
        user_query = db.query(models.User).filter(models.User.id == current_user.id)
        user_query.update(newSelf.dict(exclude_unset=True), synchronize_session= False)

        db.commit()

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown Error")
            
    else:
        return user_query.first()