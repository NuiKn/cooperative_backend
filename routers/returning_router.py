from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from models.returning_model import Returning
from controllers.returning_controller import ReturningController
from schemas.returning_schema import ReturningCreate, ReturningResponse
from database import get_db

router = APIRouter()


@router.post("/returning/all", response_model=None)
def create_returning(booking_id: int, db: Session = Depends(get_db)):
    controller = ReturningController(db)
    return controller.create_returning_all(booking_id)



@router.get("/returning/{booking_id}", response_model=List[ReturningResponse])
def read_returnings(booking_id: int, db: Session = Depends(get_db)):
    controller = ReturningController(db)
    return controller.get_returnings_by_booking_id(booking_id)

@router.get("/admin/returnings/", response_model=List[ReturningResponse]) 
def read_all_returnings_admin(db: Session = Depends(get_db)):
    controller = ReturningController(db)
    return controller.get_all_returnings_admin()

