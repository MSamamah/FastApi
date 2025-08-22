from fastapi import APIRouter
from app.controllers.shopify.orders.orders_count_controller import fetch_orders_count
from app.models.shopify.orders.orders_count import OrdersCountResponse

router = APIRouter()

@router.get("/orders/count", response_model=OrdersCountResponse)
def get_orders_count():
    """
    Fetch total number of Shopify orders.
    """
    return fetch_orders_count()
