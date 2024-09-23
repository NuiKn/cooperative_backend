from fastapi import APIRouter, Depends, HTTPException ,status, Request
from sqlalchemy.orm import Session
#from database.connection import get_db
from database import get_db
from controllers.user_controller import UserController
from schemas.user_schema import UserCreate, UserUpdate, UserOut
from typing import List
from middleware import check_permissions , decode_token

router = APIRouter()

""" @router.get("/", response_model=List[UserOut])
def read_all_users(db: Session = Depends(get_db)):
    return UserController.get_all_users(db)


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return UserController.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return UserController.update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    return UserController.delete_user(db, user_id) """

#### ใช้ token และมีการ login

#อ่าน user ทุกคน โดย admin
@router.get("/", response_model=List[UserOut])
async def read_all_users(db: Session = Depends(get_db), role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return UserController.get_all_users(db)

@router.get("/me", response_model=UserOut)
async def read_me(request: Request, db: Session = Depends(get_db)):
    # ดึง token จาก Cookies หรือ Authorization header
    token = request.cookies.get("access_token") or request.headers.get("Authorization").split(" ")[1]
    
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    # Decode token เพื่อดึง user_id ออกมา
    user_id = decode_token(token)
    
    return UserController.get_user(db, user_id)

@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db), role: str = Depends(check_permissions)):
    return UserController.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserOut)
async def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return UserController.update_user(db, user_id, user)

@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: Session = Depends(get_db), role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return UserController.delete_user(db, user_id)


#######
""" @router.get("/", response_model=List[UserOut])
def read_all_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # คุณสามารถตรวจสอบ token ที่นี่ได้หากจำเป็น
    return UserController.get_all_users(db)

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return UserController.get_user(db, user_id) """
