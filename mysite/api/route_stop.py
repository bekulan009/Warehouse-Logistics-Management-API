from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import RouteStop
from mysite.database.schema import RouteStopSchema, RouteStopCreateSchema

route_stop_router = APIRouter(prefix='/route-stop', tags=['RouteStop'])


@route_stop_router.post('/', response_model=RouteStopSchema)
async def create_route_stop(route_stop: RouteStopCreateSchema, db: Session = Depends(get_db)):
    route_stop_db = RouteStop(**route_stop.model_dump())
    db.add(route_stop_db)
    db.commit()
    db.refresh(route_stop_db)
    return route_stop_db


@route_stop_router.get('/', response_model=List[RouteStopSchema])
async def list_route_stop(db: Session = Depends(get_db)):
    return db.query(RouteStop).all()


@route_stop_router.get('/{route_stop_id}', response_model=RouteStopSchema)
async def detail_route_stop(route_stop_id: int, db: Session = Depends(get_db)):
    route_stop_db = db.query(RouteStop).filter(RouteStop.id == route_stop_id).first()
    if not route_stop_db:
        raise HTTPException(status_code=404, detail='RouteStop not found')
    return route_stop_db


@route_stop_router.put('/{route_stop_id}', response_model=dict)
async def update_route_stop(route_stop_id: int, route_stop: RouteStopCreateSchema, db: Session = Depends(get_db)):
    route_stop_db = db.query(RouteStop).filter(RouteStop.id == route_stop_id).first()
    if not route_stop_db:
        raise HTTPException(status_code=404, detail='RouteStop not found')

    for key, value in route_stop.model_dump().items():
        setattr(route_stop_db, key, value)

    db.commit()
    db.refresh(route_stop_db)
    return {'message': 'Updated'}


@route_stop_router.delete('/{route_stop_id}', response_model=dict)
async def delete_route_stop(route_stop_id: int, db: Session = Depends(get_db)):
    route_stop_db = db.query(RouteStop).filter(RouteStop.id == route_stop_id).first()
    if not route_stop_db:
        raise HTTPException(status_code=404, detail='RouteStop not found')

    db.delete(route_stop_db)
    db.commit()
    return {'message': 'Deleted'}
