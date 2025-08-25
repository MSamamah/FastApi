from fastapi import FastAPI
from app.routes.shopify.orders import (
    orders_routes,
    orders_count_routes,
    order_by_id_routes,
)
from app.middlewares.registry import registry
from app.middlewares.master_middleware import master_middleware

app = FastAPI(title="Shopify API Service")

# Import middleware groups to register them
from app.middlewares import groups

# Assign middleware groups to routes
registry.assign_to_route("/shopify/orders", ["orders_all"])
registry.assign_to_route("/shopify/orders/count", ["orders_count"])
registry.assign_to_route("/shopify/order", ["orders_all"])

# Apply the master middleware
app.middleware("http")(master_middleware)

@app.get("/")
def root():
    return {"message": "Shopify API Service is running"}

# Include routers
app.include_router(orders_routes.router, prefix="/shopify", tags=["Shopify - Orders"])
app.include_router(orders_count_routes.router, prefix="/shopify", tags=["Shopify - Orders Count"])
app.include_router(order_by_id_routes.router, prefix="/shopify", tags=["Shopify - Order By ID"])