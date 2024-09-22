from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 

# class BookingDetail(Base):
#     __tablename__ = 'booking_detail'
    
#     booking_detail_id = Column(Integer, primary_key=True, index=True)
#     booking_id = Column(Integer, ForeignKey('booking.booking_id'))
#     place_equipment_id = Column(Integer, ForeignKey('place_equipment.place_equipment_id'))
#     booking_quantity = Column(Integer, nullable=False)

#     booking = relationship("Booking")  # เชื่อมโยงกับ Booking
#     place_equipment = relationship("PlaceEquipment")  # เชื่อมโยงกับ PlaceEquipment

class BookingDetail(Base):
    __tablename__ = 'booking_detail'

    booking_detail_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('booking.booking_id', ondelete='CASCADE'))  # ใช้ ondelete='CASCADE'

    place_equipment_id = Column(Integer, ForeignKey("place_equipment.place_equipment_id", ondelete="CASCADE"), nullable=False)
    booking_quantity = Column(Integer, nullable=False)

    booking = relationship("Booking", back_populates="booking_details")  # เพิ่มความสัมพันธ์
    # returnings = relationship("Returning", back_populates="booking_detail")
    returnings = relationship("Returning", uselist=False , backref="booking_detail")