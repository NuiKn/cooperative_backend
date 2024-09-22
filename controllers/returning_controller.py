from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.equipment_model import Equipment
from models.placeEquipment_model import PlaceEquipment
from models.returning_model import Returning
from models.booking_detail_model import BookingDetail
from models.booking_model import Booking 
from schemas.returning_schema import ReturningCreate, ReturningCreateCustom
from schemas.returning_schema import ReturningResponse 
from sqlalchemy.orm import joinedload
import datetime
import requests
from requests.exceptions import RequestException

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
            booking = self.db.query(Booking).filter(Booking.booking_id == booking_id).first()

            # ตรวจสอบว่าพบ booking หรือไม่
            if not booking:
                return {"message": "No booking found for this booking_id"}
            
            # ตรวจสอบสถานะ booking_status
            if booking.booking_status == "คืนครบ":
                raise ValueError(400, "Cannot return items: booking has already been fully returned.")
        
            # ดึงรายการ BookingDetail ที่เกี่ยวข้องกับ booking_id นี้
            booking_details = self.db.query(BookingDetail).filter(BookingDetail.booking_id == booking_id).all()
        
            # ตรวจสอบว่าพบ booking_details หรือไม่
            if not booking_details:
                return {"message": "No booking details found for this booking_id"}

            # ลูปผ่าน booking_details และสร้าง returning สำหรับแต่ละรายการ
            
            for detail in booking_details:
                print(detail.__dict__)
                # ตรวจสอบว่ามี PlaceEquipment หรือไม่
                equipment_place = self.db.query(PlaceEquipment).filter_by(place_equipment_id=detail.place_equipment_id).first()
                if equipment_place is None:
                    raise ValueError(404, "Equipment not found") 
                
                over = equipment_place.available_stock + detail.booking_quantity
                # ตรวจสอบว่าไม่เกิน stock
                if over > equipment_place.stock:
                    raise ValueError(400, "Over stock available")

                # เพิ่มจำนวน available_stock
                equipment_place.available_stock += detail.booking_quantity

                new_returning = Returning(
                    booking_detail_id=detail.booking_detail_id,
                    returning_time=datetime.datetime.now(),
                    returning_quantity=detail.booking_quantity   
                )
                
                self.db.add(new_returning)
            booking_to_update = self.db.query(Booking).filter(Booking.booking_id == booking_id).first()
            if booking_to_update:
                booking_to_update.booking_status = "คืนครบ"
                self.db.add(booking_to_update)
            # Commit transaction
            self.db.commit()

            return {"message": "Returnings created successfully"}


        except Exception as e:
            self.db.rollback()  # ยกเลิกการเปลี่ยนแปลงถ้าเกิดข้อผิดพลาด
            return {"error": str(e)}
        
    





 

    def create_returning(self, returning: ReturningCreateCustom):
        try:
            # เริ่ม transaction
            self.db.begin()
            
            url = f"http://127.0.0.1:8000/booking/{returning.booking_id}?user_id={returning.user_id}"
            response = requests.get(url)

            # ตรวจสอบสถานะการตอบกลับ
            if response.status_code == 200:
                data = response.json()
                booking_detail = data["booking_detail"]
                # print(booking_detail)

                # เช็ค place_equipment_id ว่าตรงกันไหม
                # for equipment in returning.equipments:
                for index, equipment in enumerate(returning.equipments):
                    if any(detail['place_equipment_id'] == equipment.place_equipment_id for detail in booking_detail):
                        equipment_place = self.db.query(PlaceEquipment).filter_by(place_equipment_id=equipment.place_equipment_id).first()
                        print("xxx") 
                        print(f"booking_detail[index]['booking_quantity']: {booking_detail[index]['booking_quantity']}") 
                        print(f"(equipment.returning_quantity+booking_detail[index]['returning_quantity']): { (equipment.returning_quantity+booking_detail[index]['returning_quantity']) }") 
                        print(f"(equipment.returning_quantity): { (equipment.returning_quantity) }")
                        print(f"(booking_detail[index]['returning_quantity']): {booking_detail[index]['returning_quantity'] }")
                        if(booking_detail[index]['booking_quantity'] > (equipment.returning_quantity+booking_detail[index]['returning_quantity'])):
                            equipment_place.available_stock+=equipment.returning_quantity
                        else:
                            self.db.rollback()
                            raise HTTPException(status_code=400, detail="you return over.")
                        # เพิ่มข้อมูลลงในฐานข้อมูล
                        # สร้าง instance ของ returning ที่จะเพิ่ม
                        print(equipment)
                        print(booking_detail[index]['booking_detail_id'])
                        new_returning = Returning(
                            booking_detail_id= booking_detail[index]['booking_detail_id'],
                            returning_quantity=equipment.returning_quantity,
                            returning_time=datetime.datetime.now()
                        )
                        print("xxx") 
                        self.db.add(new_returning)
                    else:
                        # ถ้าไม่ตรงให้ rollback
                        self.db.rollback()
                        raise HTTPException(status_code=400, detail="place_equipment_id does not match.")

                # Commit transaction ถ้าทุกอย่างเรียบร้อย
                self.db.commit()
                return {"message": "Success", "booking_detail": booking_detail}
            else:
                raise HTTPException(status_code=response.status_code, detail=f"Error: {response.status_code}")

        except RequestException as e:
            print(f"Request error occurred: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Request failed.") 
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occurred.")







    
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # def create_returning(self, returning: ReturningCreateCustom):
    #     try:
    #         url = f"http://127.0.0.1:8000/booking/{returning.booking_id}?user_id={returning.user_id}"
    #         response = requests.get(url)
    #         booking_detail = None
    #         # ตรวจสอบสถานะการตอบกลับ
    #         if response.status_code == 200:
    #             data = response.json() 
    #             booking_detail = data["booking_detail"]
    #             print(booking_detail)
    #             return {"message": "Success", "booking_detail": booking_detail}  # ส่งกลับข้อมูล
    #         else:
    #             raise HTTPException(status_code=response.status_code, detail=f"Error: {response.status_code}")

    #     except RequestException as e:
    #         print(f"Request error occurred: {e}")
    #         raise HTTPException(status_code=500, detail="Request failed.")
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         raise HTTPException(status_code=500, detail="An error occurred.")



        
    #  backup_create_returning
    # def create_returning(self, returning_data):
    #     try:
    #         # ตรวจสอบว่ามี booking_id นี้หรือไม่
    #         booking_id = returning_data.booking_id
    #         booking_details = self.db.query(BookingDetail).filter_by(booking_id=booking_id).all()

    #         if not booking_details:
    #             raise HTTPException(status_code=404, detail="Booking not found")

    #         # วนลูปบันทึกการคืนสำหรับอุปกรณ์แต่ละรายการ
    #         for equipment in returning_data.equipments:
    #             # ค้นหา booking_detail ที่ตรงกับ place_equipment_id และ booking_id
    #             booking_detail = self.db.query(BookingDetail).filter(
    #                 BookingDetail.place_equipment_id == equipment.place_equipment_id,
    #                 BookingDetail.booking_id == booking_id
    #             ).first()

    #             if not booking_detail:
    #                 raise HTTPException(status_code=404, detail=f"Booking detail not found for equipment id {equipment.place_equipment_id}")

    #             # # เช็คว่า equipment.booking_quantity <= booking_detail.booking_quantity
    #             # if equipment.booking_quantity > booking_detail.booking_quantity:
    #             #     raise HTTPException(
    #             #         status_code=400, 
    #             #         detail=f"Returning quantity {equipment.booking_quantity} exceeds borrowed quantity {booking_detail.booking_quantity} for equipment id {equipment.place_equipment_id}"
    #             #     )


    #             # สร้าง returning record
    #             new_returning = Returning(
    #                 booking_detail_id=booking_detail.booking_detail_id,
    #                 returning_quantity=equipment.booking_quantity,
    #                 returning_time=datetime.datetime.now()  # อาจใช้เวลาปัจจุบัน
    #             )

    #             self.db.add(new_returning)

    #         # บันทึกข้อมูลทั้งหมดลงในฐานข้อมูล
    #         self.db.commit()
    #         return {"message": "Returning created successfully"}

    #     except Exception as e:
    #         self.db.rollback()
    #         raise HTTPException(status_code=500, detail=str(e))





