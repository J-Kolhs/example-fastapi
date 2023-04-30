from fastapi import status, HTTPException, APIRouter, Depends, Response
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from .. import schemas, models, oauth2

# The router is created using APIRouter from fastapi, with a prefix of /access and a tag of Access.
router = APIRouter(
    prefix = "/access",
    tags = ["Access"]
)

# The first route defined is a POST method that creates new access records.
# It takes in a list of schemas.AccessBase objects, a database session, and the current user obtained from the oauth2.get_current_user dependency.
# It returns a list of newly created schemas.AccessOut objects.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= List[schemas.AccessOut])
def create_access(access: List[schemas.AccessBase], db: Session = Depends((get_db)), current_user: dict = Depends(oauth2.get_current_user)):

           
    if current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only Admins can create access")

   
    new_access = [models.Access(room_id = i.room_id, user_id  = i.user_id) for i in access]
    

    try:
        [db.add(i) for i in new_access]
        db.commit()
        [db.refresh(i) for i in new_access ]

    except IntegrityError as e:
        print(e.orig)
        if type(e.orig) == UniqueViolation:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail =  str(e.orig) )    
        if type(e.orig) == ForeignKeyViolation:
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail = str(e.orig))
    else:
        return new_access

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_access(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    access_query = db.query(models.Access).filter(models.Access.id == id)
    access = access_query.first()

    if access == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Access with id {id} does not exist")
    if current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only Admins can delete access")

    access_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{room_id}", status_code=status.HTTP_200_OK, response_model= List[schemas.AccessView])
def get_access(room_id: int, db: Session = Depends((get_db)), current_user: dict = Depends(oauth2.get_current_user)):
    
    access = db.query(models.Access).filter(models.Access.room_id == room_id).all()

    if current_user.roles == 'ADMIN':
        return access

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"You are not authorized to manage access for room {room_id}")

@router.get("/self/")
def get_self_access(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    access = []
    
    for room_access in current_user.access:
        access.append(room_access.room_id)

    return set(access)