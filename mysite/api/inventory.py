from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Inventory
from mysite.database.schema import InventorySchema, InventoryCreateSchema

inventory_router = APIRouter(prefix='/inventory', tags=['Inventory'])


@inventory_router.post('/', response_model=InventorySchema)
async def create_inventory(inventory: InventoryCreateSchema, db: Session = Depends(get_db)):
    inventory_db = Inventory(**inventory.model_dump())
    db.add(inventory_db)
    db.commit()
    db.refresh(inventory_db)
    return inventory_db


@inventory_router.get('/', response_model=List[InventorySchema])
async def list_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@inventory_router.get('/{inventory_id}', response_model=InventorySchema)
async def detail_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(status_code=404, detail='Inventory not found')
    return inventory_db


@inventory_router.put('/{inventory_id}', response_model=dict)
async def update_inventory(inventory_id: int, inventory: InventoryCreateSchema, db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(status_code=404, detail='Inventory not found')

    for key, value in inventory.model_dump().items():
        setattr(inventory_db, key, value)

    db.commit()
    db.refresh(inventory_db)
    return {'message': 'Updated'}


@inventory_router.delete('/{inventory_id}', response_model=dict)
async def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory_db = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory_db:
        raise HTTPException(status_code=404, detail='Inventory not found')

    db.delete(inventory_db)
    db.commit()
    return {'message': 'Deleted'}
