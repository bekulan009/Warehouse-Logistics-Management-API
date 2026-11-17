from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Courier
from mysite.database.schema import CourierSchema, CourierCreateSchema

courier_router = APIRouter(prefix='/courier', tags=['Courier'])


@courier_router.post('/', response_model=CourierSchema)
async def create_courier(courier: CourierCreateSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.model_dump())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.get('/', response_model=List[CourierSchema])
async def list_courier(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@courier_router.get('/{courier_id}', response_model=CourierSchema)
async def detail_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(status_code=404, detail='Courier not found')
    return courier_db


@courier_router.put('/{courier_id}', response_model=dict)
async def update_courier(courier_id: int, courier: CourierCreateSchema, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(status_code=404, detail='Courier not found')

    for key, value in courier.model_dump().items():
        setattr(courier_db, key, value)

    db.commit()
    db.refresh(courier_db)
    return {'message': 'Updated'}


@courier_router.delete('/{courier_id}', response_model=dict)
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(status_code=404, detail='Courier not found')

    db.delete(courier_db)
    db.commit()
    return {'message': 'Deleted'}
