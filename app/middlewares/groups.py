from .registry import registry
from .global_middleware import global_middleware
from .shopify.orders.orders_middleware import orders_middleware
from .shopify.orders.orders_count_middleware import orders_count_middleware

# Register middleware groups
registry.register_group("global", [global_middleware])
registry.register_group("orders", [orders_middleware])
registry.register_group("orders_count", [orders_count_middleware])
registry.register_group("orders_all", [global_middleware, orders_middleware])