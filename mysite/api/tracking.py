from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import TrackingEvent
from mysite.database.schema import TrackingEventSchema, TrackingEventCreateSchema

tracking_router = APIRouter(prefix='/tracking', tags=['TrackingEvent'])


@tracking_router.post('/', response_model=TrackingEventSchema)
async def create_tracking_event(event: TrackingEventCreateSchema, db: Session = Depends(get_db)):
    event_db = TrackingEvent(**event.model_dump())
    db.add(event_db)
    db.commit()
    db.refresh(event_db)
    return event_db


@tracking_router.get('/', response_model=List[TrackingEventSchema])
async def list_tracking_event(db: Session = Depends(get_db)):
    return db.query(TrackingEvent).all()


@tracking_router.get('/{event_id}', response_model=TrackingEventSchema)
async def detail_tracking_event(event_id: int, db: Session = Depends(get_db)):
    event_db = db.query(TrackingEvent).filter(TrackingEvent.id == event_id).first()
    if not event_db:
        raise HTTPException(status_code=404, detail='TrackingEvent not found')
    return event_db


@tracking_router.put('/{event_id}', response_model=dict)
async def update_tracking_event(event_id: int, event: TrackingEventCreateSchema, db: Session = Depends(get_db)):
    event_db = db.query(TrackingEvent).filter(TrackingEvent.id == event_id).first()
    if not event_db:
        raise HTTPException(status_code=404, detail='TrackingEvent not found')

    for key, value in event.model_dump().items():
        setattr(event_db, key, value)

    db.commit()
    db.refresh(event_db)
    return {'message': 'Updated'}


@tracking_router.delete('/{event_id}', response_model=dict)
async def delete_tracking_event(event_id: int, db: Session = Depends(get_db)):
    event_db = db.query(TrackingEvent).filter(TrackingEvent.id == event_id).first()
    if not event_db:
        raise HTTPException(status_code=404, detail='TrackingEvent not found')

    db.delete(event_db)
    db.commit()
    return {'message': 'Deleted'}
