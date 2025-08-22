from fastapi import FastAPI
from app.routes.shopify.orders import (
    orders_routes,
    orders_count_routes,
    order_by_id_routes,
)

app = FastAPI(title="Shopify API Service")


@app.get("/")
def root():
    return {"message": "Shopify API Service is running"}


app.include_router(orders_routes.router, prefix="/shopify", tags=["Shopify - Orders"])
app.include_router(orders_count_routes.router, prefix="/shopify", tags=["Shopify - Orders Count"])
app.include_router(order_by_id_routes.router, prefix="/shopify", tags=["Shopify - Order By ID"])
