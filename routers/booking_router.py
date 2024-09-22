from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db 
from schemas.booking_schema import BookingCreate, Booking ,BookingResponse,BookingDetailBaseCreateUser
from controllers.booking_controller import BookingController
from typing import List

router = APIRouter()


# finish
# @router.post("/admin/booking/", response_model=Booking)
# def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
#     controller = BookingController(db)
#     return controller.create_booking(booking)
    

# finish
@router.get("/admin/bookings/", response_model=List[BookingResponse])
def read_bookings_admin(user_id:int =None ,page: int =None, limit: int =None, db: Session = Depends(get_db)): 
    controller = BookingController(db)
    return controller.get_bookings(user_id,page=page, limit=limit)


# finish
@router.put("/admin/booking/{booking_id}", response_model=Booking)
def update_booking_status_admin(booking_id: int, status: str, note: str, db: Session = Depends(get_db)):
    controller = BookingController(db)
    return controller.update_booking_status_admin(booking_id, status,note)

# finish
@router.delete("/admin/booking/{booking_id}", response_model=int)
def delete_booking_admin(booking_id: int, db: Session = Depends(get_db)):
    controller = BookingController(db)
    return controller.delete_booking_admin(booking_id)

# finish
@router.post("/user/booking/", response_model=Booking)
def create_booking_user(booking_details: List[BookingDetailBaseCreateUser], db: Session = Depends(get_db)):
    controller = BookingController(db)
    return controller.create_booking_user(booking_details)

# finish
@router.get("/booking/{booking_id}", response_model=BookingResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    controller = BookingController(db)
    return controller.get_booking(booking_id)


@router.get("/bookings/", response_model=List[BookingResponse])
def read_bookings(user_id: int ,page: int =None, limit: int =None, db: Session = Depends(get_db)):
    controller = BookingController(db)
    return controller.get_bookings(user_id=user_id, page=page, limit=limit)

 



 







# @router.get("/bookings/", response_model=List[Booking])
# def read_bookings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     controller = BookingController(db)
#     return controller.get_bookings(skip=skip, limit=limit)

# @router.get("/booking/{booking_id}", response_model=Booking)
# def read_booking(booking_id: int, db: Session = Depends(get_db)):
#     controller = BookingController(db)
#     return controller.get_booking(booking_id)

