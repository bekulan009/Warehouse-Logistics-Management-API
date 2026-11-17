from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Warehouse
from mysite.database.schema import WarehouseSchema, WarehouseCreateSchema

warehouse_router = APIRouter(prefix='/warehouse', tags=['Warehouse'])


@warehouse_router.post('/', response_model=WarehouseSchema)
async def create_warehouse(warehouse: WarehouseCreateSchema, db: Session = Depends(get_db)):
    warehouse_db = Warehouse(**warehouse.model_dump())
    db.add(warehouse_db)
    db.commit()
    db.refresh(warehouse_db)
    return warehouse_db


@warehouse_router.get('/', response_model=List[WarehouseSchema])
async def list_warehouse(db: Session = Depends(get_db)):
    return db.query(Warehouse).all()


@warehouse_router.get('/{warehouse_id}', response_model=WarehouseSchema)
async def detail_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(status_code=404, detail='Warehouse not found')
    return warehouse_db


@warehouse_router.put('/{warehouse_id}', response_model=dict)
async def update_warehouse(warehouse_id: int, warehouse: WarehouseCreateSchema, db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(status_code=404, detail='Warehouse not found')

    for key, value in warehouse.model_dump().items():
        setattr(warehouse_db, key, value)

    db.commit()
    db.refresh(warehouse_db)
    return {'message': 'Updated'}


@warehouse_router.delete('/{warehouse_id}', response_model=dict)
async def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    warehouse_db = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse_db:
        raise HTTPException(status_code=404, detail='Warehouse not found')

    db.delete(warehouse_db)
    db.commit()
    return {'message': 'Deleted'}
