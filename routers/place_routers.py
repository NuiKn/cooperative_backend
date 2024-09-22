from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from controllers.place_controller import PlaceController
from middleware import check_permissions
from schemas.place_schema import PlaceCreate, PlaceUpdate, Place
from database import get_db

router = APIRouter()

@router.get("/place/", response_model=list[Place])
def getAll_place(db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    return PlaceController.getAll_place(db=db)

@router.get("/place/{place_id}", response_model=Place)
def getById_place(place_id: int, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    return PlaceController.getById_place(db=db, place_id=place_id)

#admin
@router.post("/place/", response_model=Place)
def create_place(place: PlaceCreate, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return PlaceController.create_place(db=db, place=place)

@router.put("/place/{place_id}", response_model=Place)
def update_place(place_id: int, place: PlaceUpdate, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return PlaceController.update_place(db=db, place_id=place_id, place=place)

@router.delete("/place/{place_id}", response_model=dict)
def delete_place(place_id: int, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return PlaceController.delete_place(db=db, place_id=place_id)
