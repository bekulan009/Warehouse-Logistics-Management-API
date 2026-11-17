from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import InventoryReservation
from mysite.database.schema import InventoryReservationSchema, InventoryReservationCreateSchema

reservation_router = APIRouter(prefix='/reservation', tags=['InventoryReservation'])


@reservation_router.post('/', response_model=InventoryReservationSchema)
async def create_reservation(reservation: InventoryReservationCreateSchema, db: Session = Depends(get_db)):
    reservation_db = InventoryReservation(**reservation.model_dump())
    db.add(reservation_db)
    db.commit()
    db.refresh(reservation_db)
    return reservation_db


@reservation_router.get('/', response_model=List[InventoryReservationSchema])
async def list_reservation(db: Session = Depends(get_db)):
    return db.query(InventoryReservation).all()


@reservation_router.get('/{reservation_id}', response_model=InventoryReservationSchema)
async def detail_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(status_code=404, detail='Reservation not found')
    return reservation_db


@reservation_router.put('/{reservation_id}', response_model=dict)
async def update_reservation(reservation_id: int, reservation: InventoryReservationCreateSchema, db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(status_code=404, detail='Reservation not found')

    for key, value in reservation.model_dump().items():
        setattr(reservation_db, key, value)

    db.commit()
    db.refresh(reservation_db)
    return {'message': 'Updated'}


@reservation_router.delete('/{reservation_id}', response_model=dict)
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation_db = db.query(InventoryReservation).filter(InventoryReservation.id == reservation_id).first()
    if not reservation_db:
        raise HTTPException(status_code=404, detail='Reservation not found')

    db.delete(reservation_db)
    db.commit()
    return {'message': 'Deleted'}
