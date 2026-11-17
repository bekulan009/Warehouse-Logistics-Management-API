import uvicorn
from fastapi import FastAPI
from mysite.database.db import engine, Base
from mysite.admin.setup import setup_admin
from mysite.api import (
    warehouse_router,
    inventory_router,
    reservation_router,
    courier_router,
    location_router,
    delivery_router,
    route_router,
    route_stop_router,
    tracking_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Warehouse & Logistics Management API')

setup_admin(app)

app.include_router(warehouse_router)
app.include_router(inventory_router)
app.include_router(reservation_router)
app.include_router(courier_router)
app.include_router(location_router)
app.include_router(delivery_router)
app.include_router(route_router)
app.include_router(route_stop_router)
app.include_router(tracking_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
