from fastapi import APIRouter, HTTPException
from app.services.orders.order_storage_service import get_all_orders_from_db, get_order_by_shopify_id
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class StoredOrderResponse(BaseModel):
    id: int
    shopify_order_id: str
    order_name: Optional[str]
    order_data: dict
    created_at: str
    updated_at: Optional[str]

@router.get("/storage/orders", response_model=List[StoredOrderResponse])
def get_stored_orders():
    """
    Get all orders stored in the database
    """
    orders = get_all_orders_from_db()
    return orders

@router.get("/storage/orders/{shopify_order_id}", response_model=StoredOrderResponse)
def get_stored_order(shopify_order_id: str):
    """
    Get a specific order by Shopify order ID
    """
    order = get_order_by_shopify_id(shopify_order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order