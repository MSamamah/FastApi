from sqlalchemy.orm import Session
from app.models.shopify.orders.order_storage import SessionLocal, StoredOrder
import json

def save_order_to_db(shopify_order_id: str, order_data: dict):
    db = SessionLocal()
    try:
        # Extract order name from the order data if available
        order_name = order_data.get('name', '') if isinstance(order_data, dict) else ''
        
        # Check if order already exists
        existing_order = db.query(StoredOrder).filter(
            StoredOrder.shopify_order_id == shopify_order_id
        ).first()
        
        if existing_order:
            # Update existing order
            existing_order.order_data = json.dumps(order_data)
            if order_name:
                existing_order.order_name = order_name
        else:
            # Create new order record
            new_order = StoredOrder(
                shopify_order_id=shopify_order_id,
                order_name=order_name,
                order_data=json.dumps(order_data)
            )
            db.add(new_order)
        
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error saving order to database: {str(e)}")
        return False
    finally:
        db.close()

def get_all_orders_from_db():
    db = SessionLocal()
    try:
        orders = db.query(StoredOrder).all()
        return [order.to_dict() for order in orders]
    except Exception as e:
        print(f"Error retrieving orders from database: {str(e)}")
        return []
    finally:
        db.close()

def get_order_by_shopify_id(shopify_order_id: str):
    db = SessionLocal()
    try:
        order = db.query(StoredOrder).filter(
            StoredOrder.shopify_order_id == shopify_order_id
        ).first()
        return order.to_dict() if order else None
    except Exception as e:
        print(f"Error retrieving order from database: {str(e)}")
        return None
    finally:
        db.close()