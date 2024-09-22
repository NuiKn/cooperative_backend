from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base 

class Returning(Base):
    __tablename__ = "returning"
    returning_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_detail_id = Column(Integer, ForeignKey("booking_detail.booking_detail_id", ondelete="CASCADE"), nullable=False)
    # returning_date = Column(Date, nullable=False)
    returning_time = Column(String, nullable=False)  # ใช้ String แทน Timestamp
    returning_quantity = Column(Integer, nullable=False)

    # booking_detail = relationship("BookingDetail", back_populates="returnings")