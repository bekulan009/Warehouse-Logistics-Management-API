from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import CourierLocation
from mysite.database.schema import CourierLocationSchema, CourierLocationCreateSchema

location_router = APIRouter(prefix='/location', tags=['CourierLocation'])


@location_router.post('/', response_model=CourierLocationSchema)
async def create_location(location: CourierLocationCreateSchema, db: Session = Depends(get_db)):
    location_db = CourierLocation(**location.model_dump())
    db.add(location_db)
    db.commit()
    db.refresh(location_db)
    return location_db


@location_router.get('/', response_model=List[CourierLocationSchema])
async def list_location(db: Session = Depends(get_db)):
    return db.query(CourierLocation).all()


@location_router.get('/{location_id}', response_model=CourierLocationSchema)
async def detail_location(location_id: int, db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(status_code=404, detail='Location not found')
    return location_db


@location_router.put('/{location_id}', response_model=dict)
async def update_location(location_id: int, location: CourierLocationCreateSchema, db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(status_code=404, detail='Location not found')

    for key, value in location.model_dump().items():
        setattr(location_db, key, value)

    db.commit()
    db.refresh(location_db)
    return {'message': 'Updated'}


@location_router.delete('/{location_id}', response_model=dict)
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    location_db = db.query(CourierLocation).filter(CourierLocation.id == location_id).first()
    if not location_db:
        raise HTTPException(status_code=404, detail='Location not found')

    db.delete(location_db)
    db.commit()
    return {'message': 'Deleted'}
