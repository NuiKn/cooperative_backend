from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate
import hashlib

class UserController:

    def get_user(db: Session, user_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_all_users(db: Session):
        users = db.query(User).all()
        return users

    def create_user(db: Session, user: UserCreate):
        # ตรวจสอบว่า user_name มีอยู่ในฐานข้อมูลหรือไม่
        existing_user = db.query(User).filter(User.user_name == user.user_name).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # แฮชรหัสผ่าน
        hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
        
        # ตั้งค่า role ให้เป็น 'user' โดยค่าเริ่มต้น
        db_user = User(
            user_name=user.user_name,
            password=hashed_password,
            sername=user.sername,
            lastname=user.lastname,
            tell=user.tell,
            role="user"  # ตั้ง role ให้เป็นค่าเริ่มต้น
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(db: Session, user_id: int, user: UserUpdate):
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(db: Session, user_id: int):
        db_user = db.query(User).filter(User.user_id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return {"detail": "User deleted successfully"}
