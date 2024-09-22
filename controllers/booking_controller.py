from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.booking_model import Booking
from models.booking_detail_model import BookingDetail 
from schemas.booking_schema import BookingCreate ,BookingResponse,BookingDetailBase ,BookingDetailBaseCreateUser
from sqlalchemy.exc import SQLAlchemyError
from models.placeEquipment_model import PlaceEquipment
from models.equipment_model import Equipment

from collections import OrderedDict

class BookingController:
##### admin #####
    def __init__(self, db: Session):
        self.db = db
    # def create_booking(self, booking: BookingCreate):
    #     try:
    #         print("Starting transaction...")
    #         db_booking = Booking(**booking.dict(exclude={'booking_detail'}))
    #         self.db.add(db_booking)

    #         self.db.flush()  # ทำให้ db_booking.booking_id ถูกตั้งค่าจากฐานข้อมูล
    #         print(self.db.query(Booking).count())
    #         print(f"Booking created with ID: {db_booking.booking_id}")

    #         # เพิ่ม BookingDetail สำหรับ booking นี้
    #         for detail in booking.booking_detail:
    #             # ดึงข้อมูล equipment_place ที่เกี่ยวข้อง
    #             if detail.booking_quantity<=0:
    #                 raise HTTPException(status_code=400, detail="Please enter quantity of equipment more than zero.")
    #             equipment_place = self.db.query(PlaceEquipment).filter_by(place_equipment_id=detail.place_equipment_id).first()
    #             if equipment_place is None:
    #                 raise HTTPException(status_code=404, detail="Equipment not found")

    #             if equipment_place.available_stock < detail.booking_quantity:
    #                 raise HTTPException(status_code=400, detail="Not enough stock available")

    #             # ลดจำนวน available_stock
    #             equipment_place.available_stock -= detail.booking_quantity
    #             # ไม่ต้องใช้ self.db.add(equipment_place) เพราะเราแค่ปรับค่าในอ็อบเจกต์ที่มีอยู่แล้ว

    #             # เพิ่ม BookingDetail
    #             db_booking_detail = BookingDetail(
    #                 booking_id=db_booking.booking_id,
    #                 place_equipment_id=detail.place_equipment_id,
    #                 booking_quantity=detail.booking_quantity
    #             )
    #             self.db.add(db_booking_detail)

    #         self.db.commit()
    #         print("Booking and details committed successfully")
    #         return db_booking

    #     except SQLAlchemyError as e:
    #         print(f"Error occurred: {e}")
    #         self.db.rollback()
    #         raise HTTPException(status_code=500, detail="Booking creation failed. Please enter correct format.")
            
 

    # def get_bookings_admin(self,user_id:int, page: int , limit: int):
    #     try:
    #         skip = 0  # คำนวณจำนวนที่ต้องข้าม
    #         if page ==None or limit ==None:
    #             skip = 0
    #             limit = None  
    #         elif page <= 0 :
    #             raise HTTPException(status_code=400, detail="Page must be greater than 0.")
    #         elif limit <= 0 :
    #             raise HTTPException(status_code=400, detail="Limit must be greater than 0.")
    #         else:
    #             skip = (page - 1) * limit  # คำนวณจำนวนที่ต้องข้าม
            
    #         # Query เพื่อดึงข้อมูลจากหลายตาราง
    #         bookings_with_details = (
    #             self.db.query(
    #                 Booking.booking_id,
    #                 Booking.user_id,
    #                 # Booking.booking_date,
    #                 Booking.booking_time,
    #                 Booking.booking_status,
    #                 Booking.note,
    #                 BookingDetail.place_equipment_id,
    #                 BookingDetail.booking_quantity,
    #                 Equipment.equipment_name
    #             )
    #             .join(BookingDetail, Booking.booking_id == BookingDetail.booking_id)  # Join กับ BookingDetail
    #             .join(PlaceEquipment, BookingDetail.place_equipment_id == PlaceEquipment.place_equipment_id)  # Join กับ PlaceEquipment
    #             .join(Equipment, PlaceEquipment.equipment_id == Equipment.equipment_id)  # Join กับ Equipment
    #             .offset(skip)  # ข้ามจำนวน record ตาม skip
    #             .limit(limit)  # จำกัดจำนวน record ตาม limit
    #             .all()  # ดึงข้อมูลทั้งหมด
    #         )

    #         if not bookings_with_details:
    #             raise HTTPException(status_code=404, detail="No bookings found")

    #         # จัดกลุ่มข้อมูลการจองตาม booking_id เพื่อให้ออกมาเป็น array ของการจองแต่ละรายการ
    #         bookings_data = []
    #         booking_dict = {}

    #         for detail in bookings_with_details:
    #             booking_id = detail.booking_id

    #             if booking_id not in booking_dict:
    #                 booking_dict[booking_id] = {
    #                     "user_id": detail.user_id,
    #                     # "booking_date": detail.booking_date,
    #                     "booking_time": detail.booking_time,
    #                     "booking_status": detail.booking_status,
    #                     "note": detail.note,
    #                     "booking_detail": [],
    #                     "booking_id": booking_id
    #                 }

    #             # เพิ่มรายละเอียดการจองลงใน booking_detail
    #             booking_dict[booking_id]["booking_detail"].append({
    #                 "place_equipment_id": detail.place_equipment_id,
    #                 "equipment_name": detail.equipment_name,
    #                 "booking_quantity": detail.booking_quantity
    #             })

    #         # เปลี่ยนจาก dict ไปเป็น list ของการจอง
    #         bookings_data = list(booking_dict.values())

    #         return bookings_data

    #     except SQLAlchemyError as e:
    #         print(f"Error occurred: {e}")
    #         raise HTTPException(status_code=500, detail="Error retrieving bookings.")

    def delete_booking_admin(self, booking_id: int):
        # ดึงข้อมูลการจองจากฐานข้อมูล
        booking = self.db.query(Booking).filter(Booking.booking_id == booking_id).first()
        # print(booking.__dict__)
        # ตรวจสอบว่าพบข้อมูลการจองหรือไม่
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # ลบข้อมูลการจอง
        self.db.delete(booking)
        self.db.commit()

        # ส่งคืน booking_id ที่ถูกลบ
        return booking_id  # ส่งคืน booking_id โดยตรง
    


    def update_booking_status_admin(self, booking_id: int, new_status: str, note :str):
        try:
            # ค้นหา booking ตาม ID
            booking = self.db.query(Booking).filter_by(booking_id=booking_id).first()

            if not booking:
                raise HTTPException(status_code=404, detail="Booking not found")

            # เปลี่ยนสถานะการจอง
            booking.booking_status = new_status
            booking.note = note
            self.db.commit()
            self.db.refresh(booking)

            return booking

        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Failed to update booking status")


###### user ####
    def create_booking_user(self, booking_details: List[BookingDetailBaseCreateUser]):
        try:
            print("Starting transaction...")

            # สร้างรายการ Booking ใหม่
            user_id = 1
            booking_status = "จอง"
            booking_time = datetime.now()  # ใช้เวลาปัจจุบัน
            note = "รายละเอียดการจอง"

            new_booking = Booking(
                user_id=user_id,
                booking_status=booking_status,
                booking_time=booking_time,
                note=note
            )

            # เพิ่ม booking ใหม่ลงใน database session
            self.db.add(new_booking)
            self.db.flush()  # flush เพื่อให้ booking_id ถูกตั้งค่า

            print(f"Booking created with ID: {new_booking.booking_id}")

            # สร้างรายการ BookingDetail แต่ละรายการ
            for detail in booking_details:
                if detail.booking_quantity <= 0:
                    raise ValueError(400, "Please enter quantity of equipment more than zero.") 
                     
                # ตรวจสอบว่ามี PlaceEquipment หรือไม่
                equipment_place = self.db.query(PlaceEquipment).filter_by(place_equipment_id=detail.place_equipment_id).first()
                if equipment_place is None:
                    raise ValueError(404, "Equipment not found") 

                # ตรวจสอบ stock
                if equipment_place.available_stock < detail.booking_quantity:
                    raise ValueError(400, "Not enough stock available")

                # ลดจำนวน available_stock
                equipment_place.available_stock -= detail.booking_quantity

                # สร้าง BookingDetail
                new_booking_detail = BookingDetail(
                    booking_id=new_booking.booking_id,
                    place_equipment_id=detail.place_equipment_id,
                    booking_quantity=detail.booking_quantity
                )
                self.db.add(new_booking_detail)

            # บันทึกข้อมูลทั้งหมดลงฐานข้อมูล
            self.db.commit()
            print("Booking and details committed successfully")

            return new_booking
        except ValueError as e:
            status, message = e.args
            self.db.rollback()  # Rollback ก่อน
            raise HTTPException(status_code=status, detail=message)
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            self.db.rollback()  # หากมีปัญหาเกิดขึ้นจะยกเลิกการทำ transaction ทั้งหมด
            raise HTTPException(status_code=500, detail="Booking creation failed. Please enter correct format.")

## all
    def get_bookings(self, user_id: int, page: int, limit: int):
        try:
            skip = 0  # คำนวณจำนวนที่ต้องข้าม
            if page is None or limit is None:
                skip = 0
                limit = None  
            elif page < 0:
                raise HTTPException(status_code=400, detail="Page must be greater than 0.")
            elif limit < 0:
                raise HTTPException(status_code=400, detail="Limit must be greater than 0.")
            else:
                skip = (page - 1) * limit  # คำนวณจำนวนที่ต้องข้าม
                
            # เริ่ม query
            query = self.db.query(
                Booking.booking_id,
                Booking.user_id,
                # Booking.booking_date,
                Booking.booking_time,
                Booking.booking_status,
                Booking.note,
                BookingDetail.place_equipment_id,
                BookingDetail.booking_quantity,
                Equipment.equipment_name
            ).join(BookingDetail, Booking.booking_id == BookingDetail.booking_id).join(PlaceEquipment, BookingDetail.place_equipment_id == PlaceEquipment.place_equipment_id).join(Equipment, PlaceEquipment.equipment_id == Equipment.equipment_id)

            # หาก user_id ไม่เป็น None ให้กรองข้อมูล
            if user_id is not None:
                query = query.filter(Booking.user_id == user_id)

            # ดำเนินการ offset และ limit
            bookings_with_details = query.offset(skip).limit(limit).all()

            if not bookings_with_details:
                raise HTTPException(status_code=404, detail="No bookings found")

            # จัดกลุ่มข้อมูลการจองตาม booking_id
            bookings_data = []
            booking_dict = {}

            for detail in bookings_with_details:
                booking_id = detail.booking_id

                if booking_id not in booking_dict:
                    booking_dict[booking_id] = {
                        "user_id": detail.user_id,
                        # "booking_date": detail.booking_date,
                        "booking_time": detail.booking_time,
                        "booking_status": detail.booking_status,
                        "note": detail.note,
                        "booking_detail": [],
                        "booking_id": booking_id
                    }

                # เพิ่มรายละเอียดการจองลงใน booking_detail
                booking_dict[booking_id]["booking_detail"].append({
                    "place_equipment_id": detail.place_equipment_id,
                    "equipment_name": detail.equipment_name,
                    "booking_quantity": detail.booking_quantity
                })

            # เปลี่ยนจาก dict ไปเป็น list ของการจอง
            bookings_data = list(booking_dict.values())

            return bookings_data

        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving bookings.")




# 2
    # def get_bookings(self,user_id:int, page: int , limit: int):
    #     try:
    #         skip = 0  # คำนวณจำนวนที่ต้องข้าม
    #         if page ==None or limit ==None:
    #             skip = 0
    #             limit = None  
    #         elif page <= 0 :
    #             raise HTTPException(status_code=400, detail="Page must be greater than 0.")
    #         elif limit <= 0 :
    #             raise HTTPException(status_code=400, detail="Limit must be greater than 0.")
    #         else:
    #             skip = (page - 1) * limit  # คำนวณจำนวนที่ต้องข้าม
            
    #         # Query เพื่อดึงข้อมูลจากหลายตาราง
    #         bookings_with_details = (
    #             self.db.query(
    #                 Booking.booking_id,
    #                 Booking.user_id,
    #                 # Booking.booking_date,
    #                 Booking.booking_time,
    #                 Booking.booking_status,
    #                 Booking.note,
    #                 BookingDetail.place_equipment_id,
    #                 BookingDetail.booking_quantity,
    #                 Equipment.equipment_name
    #             )
    #             .join(BookingDetail, Booking.booking_id == BookingDetail.booking_id)  # Join กับ BookingDetail
    #             .join(PlaceEquipment, BookingDetail.place_equipment_id == PlaceEquipment.place_equipment_id)  # Join กับ PlaceEquipment
    #             .join(Equipment, PlaceEquipment.equipment_id == Equipment.equipment_id)  # Join กับ Equipment
    #             .offset(skip)  # ข้ามจำนวน record ตาม skip
    #             .limit(limit)  # จำกัดจำนวน record ตาม limit
    #             .all()  # ดึงข้อมูลทั้งหมด
    #         )

    #         if not bookings_with_details:
    #             raise HTTPException(status_code=404, detail="No bookings found")

    #         # จัดกลุ่มข้อมูลการจองตาม booking_id เพื่อให้ออกมาเป็น array ของการจองแต่ละรายการ
    #         bookings_data = []
    #         booking_dict = {}

    #         for detail in bookings_with_details:
    #             booking_id = detail.booking_id

    #             if booking_id not in booking_dict:
    #                 booking_dict[booking_id] = {
    #                     "user_id": detail.user_id,
    #                     # "booking_date": detail.booking_date,
    #                     "booking_time": detail.booking_time,
    #                     "booking_status": detail.booking_status,
    #                     "note": detail.note,
    #                     "booking_detail": [],
    #                     "booking_id": booking_id
    #                 }

    #             # เพิ่มรายละเอียดการจองลงใน booking_detail
    #             booking_dict[booking_id]["booking_detail"].append({
    #                 "place_equipment_id": detail.place_equipment_id,
    #                 "equipment_name": detail.equipment_name,
    #                 "booking_quantity": detail.booking_quantity
    #             })

    #         # เปลี่ยนจาก dict ไปเป็น list ของการจอง
    #         bookings_data = list(booking_dict.values())

    #         return bookings_data

    #     except SQLAlchemyError as e:
    #         print(f"Error occurred: {e}")
    #         raise HTTPException(status_code=500, detail="Error retrieving bookings.")


 
        

    def get_booking(self, booking_id: int):
            try:
                # Query เพื่อดึงข้อมูลจากหลายตาราง
                booking_with_details = (
                    self.db.query(
                        Booking.booking_id,
                        Booking.user_id,
                        # Booking.booking_date,
                        Booking.booking_time,
                        Booking.booking_status,
                        Booking.note,
                        BookingDetail.place_equipment_id,
                        BookingDetail.booking_quantity,
                        Equipment.equipment_name
                    )
                    .join(BookingDetail, Booking.booking_id == BookingDetail.booking_id)  # Join กับ BookingDetail
                    .join(PlaceEquipment, BookingDetail.place_equipment_id == PlaceEquipment.place_equipment_id)  # Join กับ PlaceEquipment
                    .join(Equipment, PlaceEquipment.equipment_id == Equipment.equipment_id)  # Join กับ Equipment
                    .filter(Booking.booking_id == booking_id)  # กรองด้วย booking_id
                    .all()  # ดึงข้อมูลทั้งหมด
                )

                if not booking_with_details:
                    raise HTTPException(status_code=404, detail="Booking not found")

                # จัดรูปแบบข้อมูลให้อยู่ในรูปแบบ JSON ตามที่ต้องการ
                booking_data = {
                    "user_id": booking_with_details[0].user_id,
                    # "booking_date": booking_with_details[0].booking_date,
                    "booking_time": booking_with_details[0].booking_time,
                    "booking_status": booking_with_details[0].booking_status,
                    "note": booking_with_details[0].note,
                    "booking_detail": [
                        {
                            "place_equipment_id": detail.place_equipment_id,
                            "equipment_name": detail.equipment_name,
                            "booking_quantity": detail.booking_quantity
                        }
                        for detail in booking_with_details
                    ],
                    "booking_id": booking_with_details[0].booking_id
                }

                return booking_data

            except SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                raise HTTPException(status_code=500, detail="Error retrieving booking details.")

#### comment

    # def get_booking(self, booking_id: int):
    #     try:
    #         # ดึงข้อมูล booking พร้อม booking_detail ที่เกี่ยวข้อง
    #         booking_with_details = (
    #             self.db.query(Booking, BookingDetail)
    #             .join(BookingDetail, Booking.booking_id == BookingDetail.booking_id)  # INNER JOIN
    #             .filter(Booking.booking_id == booking_id)  # กรองตาม booking_id
    #             .first()  # ดึงข้อมูลแค่เรคคอร์ดเดียว
    #         )
            
    #         if not booking_with_details:
    #             raise HTTPException(status_code=404, detail="Booking not found")

    #         # แยกข้อมูล Booking และ BookingDetail
    #         booking_data = booking_with_details[0]  # ข้อมูล Booking
    #         booking_detail_data = booking_with_details[1]  # ข้อมูล BookingDetail

    #         # สร้าง BookingResponse
    #         booking_response = BookingResponse(
    #             booking_id=booking_data.booking_id,
    #             user_id=booking_data.user_id,
    #             booking_date=booking_data.booking_date,
    #             booking_time=booking_data.booking_time,
    #             booking_status=booking_data.booking_status,
    #             note=booking_data.note,
    #             booking_detail=[  # แปลงข้อมูล booking detail
    #                 BookingDetailBase(
    #                     place_equipment_id=booking_detail_data.place_equipment_id,
    #                     booking_quantity=booking_detail_data.booking_quantity
    #                 )
    #             ]
    #         )

    #         return booking_response

    #     except SQLAlchemyError as e:
    #         print(f"Error occurred: {e}")
    #         raise HTTPException(status_code=500, detail="Error retrieving booking details.")

                                    

    # def get_bookings(self, skip: int = 0, limit: int = 10):
    #     return self.db.query(Booking).offset(skip).limit(limit).all()

    # def get_booking(self, booking_id: int):
    #     booking = self.db.query(Booking).filter(Booking.booking_id == booking_id).first()
    #     if booking is None:
    #         raise HTTPException(status_code=404, detail="Booking not found")
    #     return booking
