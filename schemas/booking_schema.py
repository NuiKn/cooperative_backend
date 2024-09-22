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
    booking_detail_id: int  #################
    place_equipment_id: int
    equipment_name: Optional[str] = None  # กำหนดให้เป็น optional โดยมีค่าเริ่มต้นเป็น None
    booking_quantity: int
    returning_quantity:int         # # # # # # ถ้า เกิด errorให้แก้ตรงนี้

class BookingCreate(BookingBase): 
    booking_detail: List[BookingDetailBase]  # เพิ่ม booking_detail

class Booking(BookingBase):
    booking_id: int
    class Config:
        orm_mode = True

class BookingResponse(BookingCreate):
    booking_id: int  # เพิ่ม booking_id เพื่อให้ข้อมูลครบถ้วน
    sername:str
    lastname:str
    class Config:
        orm_mode = True
 
##Admin##


##User##

class PlaceEquipment(BaseModel):
    place_equipment_id: int
    booking_quantity: int

    
class BookingDetailBaseCreateUser(BaseModel):
    user_id:int
    detail:List[PlaceEquipment]


##User##



