from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models.returning_model import Returning
from controllers.returning_controller import ReturningController
from schemas.returning_schema import ReturningCreateCustomAll, ReturningResponse,ReturningCreateCustom
from database import get_db

router = APIRouter()

# # # # start create retrun # # # # 
# @router.post("/returning/all", response_model=None)
# def create_returning(booking_id: int, db: Session = Depends(get_db)):
#     controller = ReturningController(db)
#     return controller.create_returning_all(booking_id)

@router.post("/returning/all", response_model=None)
def create_returning(returning: ReturningCreateCustomAll, db: Session = Depends(get_db)):
    controller = ReturningController(db)
    return controller.create_returning_all2(returning)



@router.post("/returning/", response_model=None)
def create_returning(returning: ReturningCreateCustom, db: Session = Depends(get_db)):
    controller = ReturningController(db)
    return controller.create_returning(returning) 


## # # # sed create retrun # # # #  


@router.get("/returning/{booking_id}", response_model=List[ReturningResponse])
def read_returnings(booking_id: int, db: Session = Depends(get_db)):
    controller = ReturningController(db)
    return controller.get_returnings_by_booking_id(booking_id)

@router.get("/admin/returnings/", response_model=List[ReturningResponse]) 
def read_all_returnings_admin(db: Session = Depends(get_db)):
    controller = ReturningController(db)
    return controller.get_all_returnings_admin()

