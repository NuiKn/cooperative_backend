from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Booking(Base):
    __tablename__ = 'booking'
    
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    # booking_date = Column(Date, nullable=False)
    booking_time = Column(TIMESTAMP, nullable=False)
    booking_status = Column(String(255), nullable=False)
    note = Column(String(255), nullable=True)

    user = relationship("User")  # หากต้องการเชื่อมโยงกับโมเดล User
    # booking_details = relationship("BookingDetail", back_populates="booking")  # เพิ่มความสัมพันธ์
    booking_details = relationship("BookingDetail", back_populates="booking", cascade="all, delete")

