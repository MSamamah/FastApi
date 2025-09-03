from apscheduler.schedulers.background import BackgroundScheduler
from app.controllers.shopify.orders.orders_controller import fetch_orders
from app.services.orders.order_storage_service import save_order_to_db
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_store_orders():
    """Fetch orders from Shopify and store them in the database"""
    try:
        logger.info("Starting scheduled order fetch...")
        
        # Fetch orders (increase limit to get more orders if needed)
        orders_data = fetch_orders(first=250, status="status:any")
        
        # Extract orders from the response based on the actual Shopify API structure
        orders = orders_data.get('edges', []) if isinstance(orders_data, dict) else []
        
        # Counter for successfully stored orders
        stored_count = 0
        
        # Store each order in the database
        for order_edge in orders:
            order_node = order_edge.get('node', {}) if isinstance(order_edge, dict) else {}
            order_id = order_node.get('id', '')
            
            if order_id:
                # Save the complete order node data
                success = save_order_to_db(order_id, order_node)
                if success:
                    stored_count += 1
                    logger.info(f"Stored order: {order_id}")
                else:
                    logger.error(f"Failed to store order: {order_id}")
        
        logger.info(f"Completed scheduled order fetch. Processed {len(orders)} orders, stored {stored_count}.")
        
    except Exception as e:
        logger.error(f"Error in scheduled order fetch: {str(e)}")

# Create and configure the scheduler
scheduler = BackgroundScheduler()

# Add the job to run every 2 minutes
scheduler.add_job(
    fetch_and_store_orders,
    'interval',
    minutes=2,
    id='order_fetch_job',
    name='Fetch and store Shopify orders every 2 minutes',
    replace_existing=True
)

def start_scheduler():
    """Start the scheduler"""
    try:
        scheduler.start()
        logger.info("Scheduler started successfully")
        # Run immediately on startup
        fetch_and_store_orders()
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")

def shutdown_scheduler():
    """Shutdown the scheduler"""
    scheduler.shutdown()
    logger.info("Scheduler shut down successfully")