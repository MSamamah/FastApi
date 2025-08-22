from fastapi import APIRouter
from app.controllers.shopify.orders.order_by_id_controller import fetch_order_by_id
from app.models.shopify.orders.order_response import OrderResponse

router = APIRouter()

@router.get("/order/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    """
    Fetch Shopify order details by ID.
    """
    return fetch_order_by_id(order_id)
