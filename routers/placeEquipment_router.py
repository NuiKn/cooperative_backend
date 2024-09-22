from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.placeEquipment_controller import PlaceEquipmentController
from middleware import check_permissions
from schemas.placeEquipment_schema import PlaceEquipmentCreate, PlaceEquipmentUpdate, PlaceEquipment,PlaceEquipmentResponse
from database import get_db

router = APIRouter()


@router.get("/place_equipment/place/{place_id}")
def getAll_placeEquipment(place_id: int,db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    return PlaceEquipmentController.get_place_equipment_by_place_id(db=db,place_id=place_id)

@router.put("/place_equipment/{place_equipment_id}")
def update_placeEquipment(place_equipment_id: int, place_equipment: PlaceEquipmentUpdate, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    return PlaceEquipmentController.update_placeEquipment(db=db, place_equipment_id=place_equipment_id, place_equipment=place_equipment)

@router.get("/place_equipment/{place_equipment_id}", response_model=PlaceEquipmentResponse)
def getById_placeEquipment(place_equipment_id: int, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    return PlaceEquipmentController.getById_placeEquipment(db=db, place_equipment_id=place_equipment_id)

#admin
@router.get("/place_equipment/", response_model=list[PlaceEquipmentResponse])
def getAll_placeEquipment(db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return PlaceEquipmentController.getAll_placeEquipment(db=db)

@router.post("/place_equipment/")
def create_placeEquipment(place_equipment: PlaceEquipmentCreate, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return PlaceEquipmentController.create_placeEquipment(db=db, place_equipment=place_equipment)

@router.delete("/place_equipment/{place_equipment_id}", response_model=dict)
def delete_placeEquipment(place_equipment_id: int, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return PlaceEquipmentController.delete_placeEquipment(db=db, place_equipment_id=place_equipment_id)