from typing import List
from pydantic import BaseModel, Field
from datetime import date, datetime
from .booking_detail_schema import BookingDetailBase
from typing import Optional

##Admin##
class BookingBase(BaseModel):
    user_id: int 
    # booking_date: date
    booking_time: datetime
    booking_status: str
    note: Optional[str] = None
 
class BookingDetailBase(BaseModel):
    place_equipment_id: int
    equipment_name: Optional[str] = None  # กำหนดให้เป็น optional โดยมีค่าเริ่มต้นเป็น None
    booking_quantity: int

class BookingCreate(BookingBase): 
    booking_detail: List[BookingDetailBase]  # เพิ่ม booking_detail

class Booking(BookingBase):
    booking_id: int
    class Config:
        orm_mode = True

class BookingResponse(BookingCreate):
    booking_id: int  # เพิ่ม booking_id เพื่อให้ข้อมูลครบถ้วน
    class Config:
        orm_mode = True
 
##Admin##


##User##

class BookingDetailBaseCreateUser(BaseModel):
    place_equipment_id: int
    booking_quantity: int


##User##



