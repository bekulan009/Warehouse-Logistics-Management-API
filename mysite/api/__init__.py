from mysite.api.warehouse import warehouse_router
from mysite.api.inventory import inventory_router
from mysite.api.reservation import reservation_router
from mysite.api.courier import courier_router
from mysite.api.location import location_router
from mysite.api.delivery import delivery_router
from mysite.api.route import route_router
from mysite.api.route_stop import route_stop_router
from mysite.api.tracking import tracking_router

__all__ = [
    'warehouse_router',
    'inventory_router',
    'reservation_router',
    'courier_router',
    'location_router',
    'delivery_router',
    'route_router',
    'route_stop_router',
    'tracking_router'
]
