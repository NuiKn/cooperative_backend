from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
#from database.connection import get_db
from database import get_db
from controllers.auth_controller import AuthController
from controllers.user_controller import UserController
from schemas.user_schema import UserCreate, UserUpdate, UserOut
from schemas.auth_schema import LoginRequest
from datetime import timedelta
from jose import JWTError, jwt
from models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    # เรียกฟังก์ชัน create_access_token เพื่อสร้าง token และดึงข้อมูลผู้ใช้
    access_token, username, user_id, = AuthController.create_access_token(data, db=db)

    # คืนค่าพร้อม access_token, user_id, และ username
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": username
    }

@router.post("/register", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserController.create_user(db, user)

