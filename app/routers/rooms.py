from typing import List
from fastapi import status, HTTPException, APIRouter, Depends, Response
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, models, oauth2

router = APIRouter(
    prefix = "/manage_rooms",
    tags = ["Room"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model= List[schemas.RoomBase])
def get_rooms(db: Session = Depends((get_db)), current_user: dict = Depends(oauth2.get_current_user)):

    rooms = db.query(models.Room).all()

    return rooms

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.RoomOut)
def create_room(room: schemas.RoomCreate, db: Session = Depends((get_db)), current_user: dict = Depends(oauth2.get_current_user)):

    new_room = models.Room(**room.dict(), owner_id = current_user.id)
    
    try:
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        new_access = models.Access(user_id = current_user.id, room_id = new_room.id)
        db.add(new_access)
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail = f"The room name {room.room_name} is already taken!")
    else:
        return new_room
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    room_query = db.query(models.Room).filter(models.Room.id == id)
    room = room_query.first()


    if room == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Room with id {id} does not exist")

    if room.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    room_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",  response_model = schemas.RoomOut)
def update_room(id: int, room: schemas.RoomCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    try:
        room_query = db.query(models.Room).filter(models.Room.id == id)
        room_updated = room_query.first()

        if room_updated == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"Room with id {id} does not exist")

        if room_updated.owner_id != current_user.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

        room_query.update(room.dict(), synchronize_session= False)

        db.commit()

    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown Error")
            
    else:
        return room_query.first()