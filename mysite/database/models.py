from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mysite.database.db import Base


class WarehouseStatus(str, PyEnum):
    active = 'active'
    inactive = 'inactive'
    maintenance = 'maintenance'


class ReservationStatus(str, PyEnum):
    active = 'active'
    committed = 'committed'
    released = 'released'
    expired = 'expired'


class TransportType(str, PyEnum):
    walking = 'walking'
    bicycle = 'bicycle'
    motorcycle = 'motorcycle'
    car = 'car'


class CourierStatus(str, PyEnum):
    offline = 'offline'
    available = 'available'
    busy = 'busy'
    suspended = 'suspended'


class DeliveryStatus(str, PyEnum):
    pending = 'pending'
    assigned = 'assigned'
    in_transit = 'in_transit'
    delivered = 'delivered'
    cancelled = 'cancelled'


class RouteStatus(str, PyEnum):
    planned = 'planned'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class StopType(str, PyEnum):
    pickup = 'pickup'
    dropoff = 'dropoff'


class StopStatus(str, PyEnum):
    pending = 'pending'
    arrived = 'arrived'
    completed = 'completed'
    skipped = 'skipped'


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[WarehouseStatus] = mapped_column(Enum(WarehouseStatus), default=WarehouseStatus.active)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    inventories: Mapped[List['Inventory']] = relationship('Inventory', back_populates='warehouse', cascade='all, delete-orphan')
    couriers: Mapped[List['Courier']] = relationship('Courier', back_populates='warehouse')
    deliveries: Mapped[List['Delivery']] = relationship('Delivery', back_populates='warehouse')

    def __repr__(self):
        return f'{self.name} ({self.code})'


class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse.id'))
    warehouse: Mapped['Warehouse'] = relationship('Warehouse', back_populates='inventories')
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations: Mapped[List['InventoryReservation']] = relationship('InventoryReservation', back_populates='inventory', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Inventory #{self.id} Product:{self.product_id}'


class InventoryReservation(Base):
    __tablename__ = 'inventory_reservation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    inventory_id: Mapped[int] = mapped_column(ForeignKey('inventory.id'))
    inventory: Mapped['Inventory'] = relationship('Inventory', back_populates='reservations')
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[ReservationStatus] = mapped_column(Enum(ReservationStatus), default=ReservationStatus.active)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Reservation #{self.id} (Order {self.order_id})'


class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    warehouse_id: Mapped[Optional[int]] = mapped_column(ForeignKey('warehouse.id'), nullable=True)
    warehouse: Mapped[Optional['Warehouse']] = relationship('Warehouse', back_populates='couriers')
    transport_type: Mapped[TransportType] = mapped_column(Enum(TransportType), default=TransportType.car)
    status: Mapped[CourierStatus] = mapped_column(Enum(CourierStatus), default=CourierStatus.available)
    max_active_orders: Mapped[int] = mapped_column(Integer, default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    locations: Mapped[List['CourierLocation']] = relationship('CourierLocation', back_populates='courier', cascade='all, delete-orphan')
    deliveries: Mapped[List['Delivery']] = relationship('Delivery', back_populates='courier')
    routes: Mapped[List['Route']] = relationship('Route', back_populates='courier')

    def __repr__(self):
        return f'Courier #{self.id} (User {self.user_id})'


class CourierLocation(Base):
    __tablename__ = 'courier_location'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'))
    courier: Mapped['Courier'] = relationship('Courier', back_populates='locations')
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Loc #{self.id} ({self.latitude}, {self.longitude})'


class Delivery(Base):
    __tablename__ = 'delivery'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse.id'))
    warehouse: Mapped['Warehouse'] = relationship('Warehouse', back_populates='deliveries')
    courier_id: Mapped[Optional[int]] = mapped_column(ForeignKey('courier.id'), nullable=True)
    courier: Mapped[Optional['Courier']] = relationship('Courier', back_populates='deliveries')
    tracking_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    status: Mapped[DeliveryStatus] = mapped_column(Enum(DeliveryStatus), default=DeliveryStatus.pending)
    destination_address: Mapped[str] = mapped_column(String(255), nullable=False)
    destination_latitude: Mapped[float] = mapped_column(Float, nullable=False)
    destination_longitude: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_delivery_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    route_stops: Mapped[List['RouteStop']] = relationship('RouteStop', back_populates='delivery')
    tracking_events: Mapped[List['TrackingEvent']] = relationship('TrackingEvent', back_populates='delivery', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Delivery {self.tracking_code}'


class Route(Base):
    __tablename__ = 'route'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'))
    courier: Mapped['Courier'] = relationship('Courier', back_populates='routes')
    status: Mapped[RouteStatus] = mapped_column(Enum(RouteStatus), default=RouteStatus.planned)
    total_distance_km: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_duration_min: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    stops: Mapped[List['RouteStop']] = relationship('RouteStop', back_populates='route', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Route #{self.id} ({self.status})'


class RouteStop(Base):
    __tablename__ = 'route_stop'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    route_id: Mapped[int] = mapped_column(ForeignKey('route.id'))
    route: Mapped['Route'] = relationship('Route', back_populates='stops')
    delivery_id: Mapped[Optional[int]] = mapped_column(ForeignKey('delivery.id'), nullable=True)
    delivery: Mapped[Optional['Delivery']] = relationship('Delivery', back_populates='route_stops')
    stop_type: Mapped[StopType] = mapped_column(Enum(StopType), default=StopType.dropoff)
    sequence: Mapped[int] = mapped_column(Integer, default=1)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[StopStatus] = mapped_column(Enum(StopStatus), default=StopStatus.pending)
    arrived_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f'Stop #{self.id} (Seq {self.sequence})'


class TrackingEvent(Base):
    __tablename__ = 'tracking_event'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    delivery_id: Mapped[int] = mapped_column(ForeignKey('delivery.id'))
    delivery: Mapped['Delivery'] = relationship('Delivery', back_populates='tracking_events')
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'TrackingEvent #{self.id} ({self.status})'
