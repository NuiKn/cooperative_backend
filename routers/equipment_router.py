from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.equipment_controller import EquipmentController
from middleware import check_permissions
from schemas.equipment_schema import EquipmentCreate, EquipmentUpdate, Equipment
from database import get_db

router = APIRouter()

@router.get("/equipment/{equipment_id}", response_model=Equipment)
def getById_equipment(equipment_id: int, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    return EquipmentController.getById_equipment(db=db, equipment_id=equipment_id)

#admin
@router.get("/equipment/", response_model=list[Equipment])
def getAll_equipment(db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return EquipmentController.getAll_equipment(db=db)

@router.post("/equipment/", response_model=Equipment)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return EquipmentController.create_equipment(db=db, equipment=equipment)

@router.put("/equipment/{equipment_id}", response_model=Equipment)
def update_equipment(equipment_id: int, equipment: EquipmentUpdate, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return EquipmentController.update_equipment(db=db, equipment_id=equipment_id, equipment=equipment)

@router.delete("/equipment/{equipment_id}", response_model=dict)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db),role: str = Depends(check_permissions)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return EquipmentController.delete_equipment(db=db, equipment_id=equipment_id)
