from pydantic import BaseModel
from typing import Optional

class BookingDetailBase(BaseModel):
    # booking_id: Optional[int] = None  # ทำให้ booking_id เป็น optional
    place_equipment_id: int
    booking_quantity: int

class BookingDetailCreate(BookingDetailBase):
    pass

class BookingDetail(BookingDetailBase):
    booking_detail_id: int

    class Config:
        orm_mode = True
