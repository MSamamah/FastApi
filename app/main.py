from fastapi import FastAPI
from app.routes.shopify.orders import (
    orders_routes,
    orders_count_routes,
    order_by_id_routes,
)
from app.middlewares.registry import registry
from app.middlewares.master_middleware import master_middleware
from app.services.cron.cron_service import start_scheduler, shutdown_scheduler
from contextlib import asynccontextmanager
from app.routes.shopify.orders.order_storage_routes import router as storage_router

# Import middleware groups to register them
from app.middlewares import groups

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start the scheduler
    start_scheduler()
    yield
    # Shutdown: stop the scheduler
    shutdown_scheduler()

app = FastAPI(
    title="Shopify API Service",
    lifespan=lifespan
)

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
app.include_router(storage_router, prefix="/storage", tags=["Order Storage"])