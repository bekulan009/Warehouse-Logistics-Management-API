from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Delivery
from mysite.database.schema import DeliverySchema, DeliveryCreateSchema

delivery_router = APIRouter(prefix='/delivery', tags=['Delivery'])


@delivery_router.post('/', response_model=DeliverySchema)
async def create_delivery(delivery: DeliveryCreateSchema, db: Session = Depends(get_db)):
    delivery_db = Delivery(**delivery.model_dump())
    db.add(delivery_db)
    db.commit()
    db.refresh(delivery_db)
    return delivery_db


@delivery_router.get('/', response_model=List[DeliverySchema])
async def list_delivery(db: Session = Depends(get_db)):
    return db.query(Delivery).all()


@delivery_router.get('/{delivery_id}', response_model=DeliverySchema)
async def detail_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(status_code=404, detail='Delivery not found')
    return delivery_db


@delivery_router.put('/{delivery_id}', response_model=dict)
async def update_delivery(delivery_id: int, delivery: DeliveryCreateSchema, db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(status_code=404, detail='Delivery not found')

    for key, value in delivery.model_dump().items():
        setattr(delivery_db, key, value)

    db.commit()
    db.refresh(delivery_db)
    return {'message': 'Updated'}


@delivery_router.delete('/{delivery_id}', response_model=dict)
async def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery_db = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery_db:
        raise HTTPException(status_code=404, detail='Delivery not found')

    db.delete(delivery_db)
    db.commit()
    return {'message': 'Deleted'}
