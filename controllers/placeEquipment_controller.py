from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from sqlalchemy import select
from models.placeEquipment_model import PlaceEquipment
from models.equipment_model import Equipment
from models.place_model import Place
from schemas.placeEquipment_schema import PlaceEquipmentCreate, PlaceEquipmentUpdate

class PlaceEquipmentController:

    @staticmethod
    def getAll_placeEquipment(db: Session):
        place_equipments = db.query(PlaceEquipment).options(
                            joinedload(PlaceEquipment.place),
                            joinedload(PlaceEquipment.equipment)).all()
        
        
        return place_equipments
    
    @staticmethod
    def get_place_equipment_by_place_id(db: Session, place_id: int):
        """ place_equipments = db.query(PlaceEquipment).filter(PlaceEquipment.place_id == place_id).options(
                                joinedload(PlaceEquipment.equipment)).all() """
        """ return place_equipments """
        """ stmt = select(PlaceEquipment).join(Place).join(Equipment).where(Place.place_id == place_id)
        results = db.execute(stmt).scalars().all()
        print(results)
        
        return [{"place_id": pe.place_id, "equipment_name": pe.place_equipment_id} for pe in results] """
        stmt = (
        select(Place.place_name, Equipment.equipment_name ,PlaceEquipment.available_stock)
        .join(PlaceEquipment, Place.place_id == PlaceEquipment.place_id)
        .join(Equipment, PlaceEquipment.equipment_id == Equipment.equipment_id)
        .where(Place.place_id == place_id)
        )
        results = db.execute(stmt).all()
        print(results)


        
        return [{"place_name": place_name, "equipment_name": equipment_name ,"available_stock": available_stock} for place_name, equipment_name,available_stock in results]
        

    @staticmethod
    def create_placeEquipment(db: Session, place_equipment: PlaceEquipmentCreate):
        db_place_equipment = PlaceEquipment(**place_equipment.dict())
        existing_equipment = db.query(Equipment).filter(Equipment.equipment_id == place_equipment.equipment_id).first()
        existing_place = db.query(Place).filter(Place.place_id == place_equipment.place_id).first()
        if existing_equipment is None or existing_place is None :
            raise HTTPException(status_code=404, detail="data not found")
        
        db.add(db_place_equipment)
        db.commit()
        db.refresh(db_place_equipment)
        return db_place_equipment

    @staticmethod
    def getById_placeEquipment(db: Session, place_equipment_id: int):
        place_equipment = db.query(PlaceEquipment).filter(PlaceEquipment.place_equipment_id == place_equipment_id).first()
        if place_equipment is None:
            raise HTTPException(status_code=404, detail="place_equipment not found")
        return place_equipment

    @staticmethod
    def update_placeEquipment(db: Session, place_equipment_id: int, place_equipment: PlaceEquipmentUpdate):
        db_place_equipment = db.query(PlaceEquipment).filter(PlaceEquipment.place_equipment_id == place_equipment_id).first()
        if db_place_equipment is None:
            raise HTTPException(status_code=404, detail="PlaceEquipment not found")

        for key, value in place_equipment.dict(exclude_unset=True).items():
            setattr(db_place_equipment, key, value)

        db.commit()
        db.refresh(db_place_equipment)
        return db_place_equipment

    @staticmethod
    def delete_placeEquipment(db: Session, place_equipment_id: int):
        db_place_equipment = db.query(PlaceEquipment).filter(PlaceEquipment.place_equipment_id == place_equipment_id).first()
        if db_place_equipment is None:
            raise HTTPException(status_code=404, detail="PlaceEquipment not found")

        db.delete(db_place_equipment)
        db.commit()
        return {"detail": "PlaceEquipment deleted"}