from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import get_db
from mysite.database.models import Route
from mysite.database.schema import RouteSchema, RouteCreateSchema

route_router = APIRouter(prefix='/route', tags=['Route'])


@route_router.post('/', response_model=RouteSchema)
async def create_route(route: RouteCreateSchema, db: Session = Depends(get_db)):
    route_db = Route(**route.model_dump())
    db.add(route_db)
    db.commit()
    db.refresh(route_db)
    return route_db


@route_router.get('/', response_model=List[RouteSchema])
async def list_route(db: Session = Depends(get_db)):
    return db.query(Route).all()


@route_router.get('/{route_id}', response_model=RouteSchema)
async def detail_route(route_id: int, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(status_code=404, detail='Route not found')
    return route_db


@route_router.put('/{route_id}', response_model=dict)
async def update_route(route_id: int, route: RouteCreateSchema, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(status_code=404, detail='Route not found')

    for key, value in route.model_dump().items():
        setattr(route_db, key, value)

    db.commit()
    db.refresh(route_db)
    return {'message': 'Updated'}


@route_router.delete('/{route_id}', response_model=dict)
async def delete_route(route_id: int, db: Session = Depends(get_db)):
    route_db = db.query(Route).filter(Route.id == route_id).first()
    if not route_db:
        raise HTTPException(status_code=404, detail='Route not found')

    db.delete(route_db)
    db.commit()
    return {'message': 'Deleted'}
