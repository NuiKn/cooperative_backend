from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.equipment_model import Equipment
from models.placeEquipment_model import PlaceEquipment
from models.returning_model import Returning
from models.booking_detail_model import BookingDetail
from models.booking_model import Booking 
from schemas.returning_schema import ReturningCreate
from schemas.returning_schema import ReturningResponse 
from sqlalchemy.orm import joinedload
import datetime

class ReturningController:
    def __init__(self, db: Session):
        self.db = db

########## admin

    def get_all_returnings_admin(self):
        try:
            results = (
                self.db.query(Returning, Booking, Equipment)
                .join(BookingDetail, BookingDetail.booking_detail_id == Returning.booking_detail_id)
                .join(Booking, Booking.booking_id == BookingDetail.booking_id)
                .join(PlaceEquipment, PlaceEquipment.place_equipment_id == BookingDetail.place_equipment_id)
                .join(Equipment, Equipment.equipment_id == PlaceEquipment.equipment_id)
                .all()
            )

            return [
                ReturningResponse(
                    returning_id=result.Returning.returning_id,
                    booking_detail_id=result.Returning.booking_detail_id,
                    returning_time=result.Returning.returning_time,
                    returning_quantity=result.Returning.returning_quantity,
                    booking_id=result.Booking.booking_id,
                    equipment_name=result.Equipment.equipment_name
                )
                for result in results
            ]
        except Exception as e:
            print(str(e))
            raise HTTPException(status_code=500, detail=str(e))



########## admin

    # def create_returning(self, returning: ReturningCreate):
    #     db_returning = Returning(**returning.dict())
    #     self.db.add(db_returning)
    #     self.db.commit()
    #     self.db.refresh(db_returning)
    #     return db_returning

    def get_returnings_by_booking_id(self, booking_id: int) :
        try:
            # Query all Returning records that belong to the given booking_id
            results = (
                self.db.query(Returning, Booking,Equipment)
                .join(BookingDetail, BookingDetail.booking_detail_id == Returning.booking_detail_id)
                .join(Booking, Booking.booking_id == BookingDetail.booking_id)
                .join(PlaceEquipment, PlaceEquipment.place_equipment_id == BookingDetail.place_equipment_id)
                .join(Equipment, Equipment.equipment_id == PlaceEquipment.equipment_id)
                .filter(Booking.booking_id == booking_id)
                .all()
            )

            # Map results to the response structure
            if not results:
                raise HTTPException(status_code=404, detail="No returnings found for this booking_id")

        
            return [
                ReturningResponse(
                    returning_id=result.Returning.returning_id,
                    booking_detail_id=result.Returning.booking_detail_id,
                    returning_time=result.Returning.returning_time,
                    returning_quantity=result.Returning.returning_quantity,
                    booking_id=result.Booking.booking_id,
                    equipment_name=result.Equipment.equipment_name
                )
                for result in results
            ]
        except HTTPException as e:
            # ถ้าเกิด HTTPException ให้ส่งกลับ status และ detail ตามที่กำหนด
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(str(e))  # พิมพ์ข้อผิดพลาดที่เกิดขึ้น
            raise HTTPException(status_code=500, detail="Internal Server Error")
        

    def create_returning_all(self, booking_id: int):
        try:
            # ดึงรายการ BookingDetail ที่เกี่ยวข้องกับ booking_id นี้
            booking_details = self.db.query(BookingDetail).filter(BookingDetail.booking_id == booking_id).all()

            # ตรวจสอบว่าพบ booking_details หรือไม่
            if not booking_details:
                return {"message": "No booking details found for this booking_id"}

            # ลูปผ่าน booking_details และสร้าง returning สำหรับแต่ละรายการ
            
            for detail in booking_details:
                new_returning = Returning(
                    booking_detail_id=detail.booking_detail_id,
                    returning_time=datetime.datetime.now(),
                    returning_quantity=detail.booking_quantity   
                )
                self.db.add(new_returning)

            # Commit transaction
            self.db.commit()

            return {"message": "Returnings created successfully"}


        except Exception as e:
            self.db.rollback()  # ยกเลิกการเปลี่ยนแปลงถ้าเกิดข้อผิดพลาด
            return {"error": str(e)}