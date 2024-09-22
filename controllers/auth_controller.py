from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from models.user_model import User
from fastapi import HTTPException
import hashlib

SECRET_KEY = "thar"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthController:  

    def create_access_token(data: dict, db: Session):
        # ตรวจสอบ username และ password
        user = AuthController.authenticate_user(db, data.username, data.password)
        if user is not None:
            # เก็บข้อมูลเพิ่มเติมใน token (sub, id, role, iat, exp)
            to_encode = {
                "sub": data.username,
                "id": user.user_id,
                "role": user.role,
                "iat": datetime.utcnow(),  # เวลาที่สร้าง token
                "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # เวลาหมดอายุ
            }
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt, data.username, user.user_id, user.role
        else:
            raise HTTPException(status_code=404, detail="username or password is not valid")

    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(User).filter(User.user_name == username).first()
        if user and AuthController.hashed_check(password, user.password):
            return user
        return None

    def hashed_check(password: str, password_in_db: str):
        check = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if check == password_in_db:
            return True
        else:
            return False
