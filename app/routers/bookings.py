from typing import List, Optional
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, APIRouter, Depends
from sqlalchemy import and_, asc
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ExclusionViolation, CheckViolation
from sqlalchemy.sql.expression import func
from datetime import datetime, timezone, timedelta, date

router = APIRouter(
    prefix = "/bookings",
    tags = ["Bookings"]
)

@router.get("/room/{room_id}/details", response_model = List[schemas.Booking])
def get_bookings(room_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user),
 filterYear: int = None, filterMonth: int = None, filterDay: int = None):
    
    # Get access of current_user
    room_access = []
    [room_access.append(i.room_id) for i in current_user.access]
    
    if room_access.count(room_id) == 0 and current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to access this meeting room")

    try:
        minDateTime = datetime(filterYear, filterMonth, filterDay, 0, 0, 1)
        maxDateTime = datetime(filterYear, filterMonth, filterDay, 23, 59, 59)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail= 'Please specify a valid date')
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = 'No date value was specified in the query')


    bookings = db.query(models.Booking).filter(and_(models.Booking.meeting_end <= maxDateTime, models.Booking.meeting_start >= minDateTime))
    bookings = bookings.filter(models.Booking.room_id == room_id)
    bookings = bookings.order_by(asc("meeting_start"))
    return bookings.all()

@router.get("/room/{room_id}/summary/")
def get_bookings(room_id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user),
 filterYear: int = None, filterMonth: int = None):
    
    # Get access of current_user
    room_access = []
    [room_access.append(i.room_id) for i in current_user.access]

    if room_access.count(room_id) == 0 and current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to access this meeting room")

    try:
        minDateTime = datetime(filterYear, filterMonth, 1, 0, 0, 0)
        next_month = minDateTime.replace(day=28) + timedelta(days=4)
        maxDateTime = next_month - timedelta(days=next_month.day - 1)
    except ValueError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail= 'Please specify a valid year and month')
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail = 'No year and month values were specified in the query')

    bookings = db.query(func.distinct(func.date(models.Booking.meeting_start)).label("meeting_day")).order_by(asc("meeting_day"))
    bookings = bookings.filter(and_(models.Booking.meeting_start < maxDateTime, models.Booking.meeting_end >= minDateTime))
    bookings = bookings.filter(models.Booking.room_id == room_id)

    return bookings.all()


@router.post("/room/{room_id}", status_code=status.HTTP_201_CREATED, response_model = schemas.BookingBase)
def create_booking(room_id:int, booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    new_booking = models.Booking(owner_id = current_user.id, **booking.dict(), room_id = room_id)

    # Get access of current_user
    room_access = []
    [room_access.append(i.room_id) for i in current_user.access]

    if room_access.count(room_id) == 0 and current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to access this meeting room")

    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
    except IntegrityError as e:
        if type(e.orig) == CheckViolation:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The start time of the booking must be before its end time")
        if type(e.orig) == ExclusionViolation:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This time slot is already booked")
        else:
            print(e.orig)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown Error")
    else:
        return new_booking

@router.delete("/room/{room_id}/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(room_id: int, id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    # Get access of current_user
    room_access = []
    [room_access.append(i.room_id) for i in current_user.access]

    if room_access.count(room_id) == 0 and current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to access this meeting room")


    booking_query = db.query(models.Booking).filter(models.Booking.id == id)
    booking = booking_query.first()


    if booking == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Booking with id {id} does not exist")

    booking_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/room/{room_id}/{id}",  response_model = schemas.BookingBase)
def update_booking(room_id: int, id: int, booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    # Get access of current_user
    room_access = []
    [room_access.append(i.room_id) for i in current_user.access]

    if room_access.count(room_id) == 0 and current_user.roles != 'ADMIN':
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to access this meeting room")

    try:
        booking_query = db.query(models.Booking).filter(models.Booking.id == id)
        booking_updated = booking_query.first()

        if booking_updated == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = f"Booking with id {id} does not exist")

        if booking_updated.owner_id != current_user.id and current_user.roles != 'ADMIN':
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

        booking_query.update(booking.dict(), synchronize_session= False)

        db.commit()

    except IntegrityError as e:
        if type(e.orig) == CheckViolation:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The start time of the booking must be before its end time")
        if type(e.orig) == ExclusionViolation:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This time slot is already booked")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown Error")
            
    else:
        return booking_query.first()