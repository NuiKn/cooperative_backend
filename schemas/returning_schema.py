from pydantic import BaseModel
from typing import List, Optional
from datetime import date ,datetime

class ReturningBase(BaseModel):
    booking_detail_id: int
    # returning_date: date
    returning_time: datetime
    # returning_status: str
    returning_quantity: int

class ReturningCreate(ReturningBase):
    pass

class ReturningResponse(ReturningBase):
    returning_id: int
    booking_id: int 
    equipment_name:str
    class Config:
        orm_mode = True



# class ReturningDetail(BaseModel):
#     place_equipment_id: int
#     booking_quantity: int

# class ReturningCreate(BaseModel):
#     booking_id: int
#     returning_detail: List[ReturningDetail]  # เพิ่มรายละเอียดการคืน

# class ReturningResponse(BaseModel):
#     returning_id: int
#     booking_detail_id: int  # เพิ่ม booking_detail_id ถ้าจำเป็น

#     class Config:
#         orm_mode = True