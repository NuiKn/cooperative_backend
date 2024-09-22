from sqlalchemy import Column, Integer, String
#from database.connection import Base
from database import Base
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), unique=True, index=True)
    password = Column(String, nullable=False)
    sername = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    tell = Column(String(10), nullable=False)
    role = Column(String(255), nullable=False)
