from fastapi import APIRouter
from app.controllers.shopify.orders.orders_controller import fetch_orders
from app.models.shopify.orders.orders_response import OrdersResponse


router = APIRouter()

@router.get("/orders", response_model=OrdersResponse, name="get_orders")
def get_orders(limit: int = 10, status: str = "status:any"):
    """
    Fetch Shopify orders with optional limit and status filter.
    """
    return fetch_orders(first=limit, status=status)
