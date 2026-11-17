from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from mysite.database.models import (
    WarehouseStatus, ReservationStatus, TransportType,
    CourierStatus, DeliveryStatus, RouteStatus, StopType, StopStatus
)


class WarehouseSchema(BaseModel):
    id: int
    city_id: int
    code: str
    name: str
    street: str
    latitude: float
    longitude: float
    capacity: int
    status: WarehouseStatus
    created_at: datetime

    class Config:
        from_attributes = True


class WarehouseCreateSchema(BaseModel):
    city_id: int
    code: str
    name: str
    street: str
    latitude: float
    longitude: float
    capacity: int
    status: WarehouseStatus = WarehouseStatus.active


class InventorySchema(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    reserved_quantity: int
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryCreateSchema(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: int = 0
    reserved_quantity: int = 0


class InventoryReservationSchema(BaseModel):
    id: int
    order_id: int
    inventory_id: int
    quantity: int
    status: ReservationStatus
    expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InventoryReservationCreateSchema(BaseModel):
    order_id: int
    inventory_id: int
    quantity: int = 1
    status: ReservationStatus = ReservationStatus.active
    expires_at: Optional[datetime] = None


class CourierSchema(BaseModel):
    id: int
    user_id: int
    warehouse_id: Optional[int] = None
    transport_type: TransportType
    status: CourierStatus
    max_active_orders: int
    created_at: datetime

    class Config:
        from_attributes = True


class CourierCreateSchema(BaseModel):
    user_id: int
    warehouse_id: Optional[int] = None
    transport_type: TransportType = TransportType.car
    status: CourierStatus = CourierStatus.available
    max_active_orders: int = 3


class CourierLocationSchema(BaseModel):
    id: int
    courier_id: int
    latitude: float
    longitude: float
    recorded_at: datetime

    class Config:
        from_attributes = True


class CourierLocationCreateSchema(BaseModel):
    courier_id: int
    latitude: float
    longitude: float


class DeliverySchema(BaseModel):
    id: int
    order_id: int
    warehouse_id: int
    courier_id: Optional[int] = None
    tracking_code: str
    status: DeliveryStatus
    destination_address: str
    destination_latitude: float
    destination_longitude: float
    estimated_delivery_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DeliveryCreateSchema(BaseModel):
    order_id: int
    warehouse_id: int
    courier_id: Optional[int] = None
    tracking_code: str
    status: DeliveryStatus = DeliveryStatus.pending
    destination_address: str
    destination_latitude: float
    destination_longitude: float
    estimated_delivery_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


class RouteSchema(BaseModel):
    id: int
    courier_id: int
    status: RouteStatus
    total_distance_km: float
    estimated_duration_min: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RouteCreateSchema(BaseModel):
    courier_id: int
    status: RouteStatus = RouteStatus.planned
    total_distance_km: float = 0.0
    estimated_duration_min: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class RouteStopSchema(BaseModel):
    id: int
    route_id: int
    delivery_id: Optional[int] = None
    stop_type: StopType
    sequence: int
    latitude: float
    longitude: float
    status: StopStatus
    arrived_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RouteStopCreateSchema(BaseModel):
    route_id: int
    delivery_id: Optional[int] = None
    stop_type: StopType = StopType.dropoff
    sequence: int = 1
    latitude: float
    longitude: float
    status: StopStatus = StopStatus.pending
    arrived_at: Optional[datetime] = None


class TrackingEventSchema(BaseModel):
    id: int
    delivery_id: int
    status: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: str
    created_at: datetime

    class Config:
        from_attributes = True


class TrackingEventCreateSchema(BaseModel):
    delivery_id: int
    status: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: str
