from apscheduler.schedulers.background import BackgroundScheduler
from app.controllers.shopify.orders.orders_controller import fetch_orders
from app.services.orders.order_storage_service import save_order_to_db
from app.services.sync_state.sync_state_service import get_sync_state, update_sync_state
import logging
import traceback
from datetime import datetime
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_store_orders():
    print("*****Hello*****")
    print(datetime.now())

    # """Fetch a single batch of orders from Shopify and store them in the database"""
    # try:
    #     # Get the sync state
    #     sync_state = get_sync_state("order_fetch_job")
        
    #     # If sync is completed, don't do anything
    #     if sync_state and sync_state.is_completed:
    #         logger.info("Order sync has been completed. No more orders to fetch.")
    #         return
        
    #     # Get the last cursor from previous run
    #     after_cursor = sync_state.last_cursor if sync_state else None
    #     total_processed = sync_state.total_processed if sync_state else 0
        
    #     logger.info(f"Starting incremental order fetch. Last cursor: {after_cursor}, Total processed: {total_processed}")
        
    #     # Fetch a single batch of orders
    #     orders_data = fetch_orders(first=250, after=after_cursor, status="status:any")
        
    #     # Extract orders and page info
    #     orders = orders_data.get('edges', [])
    #     page_info = orders_data.get('pageInfo', {})
        
    #     # Store each order in the database
    #     stored_count = 0
    #     for order_edge in orders:
    #         order_node = order_edge.get('node', {})
    #         order_id = order_node.get('id', '')
            
    #         if order_id:
    #             # Save the complete order node data
    #             success = save_order_to_db(order_id, order_node)
    #             if success:
    #                 stored_count += 1
    #                 logger.debug(f"Stored order: {order_id}")
    #             else:
    #                 logger.error(f"Failed to store order: {order_id}")
        
    #     # Update counters
    #     total_processed += len(orders)
        
    #     # Check if there are more pages
    #     has_next_page = page_info.get('hasNextPage', False)
    #     end_cursor = page_info.get('endCursor')
        
    #     # Update the sync state
    #     if has_next_page:
    #         update_sync_state(
    #             "order_fetch_job", 
    #             last_cursor=end_cursor, 
    #             is_completed=False,
    #             total_processed=total_processed
    #         )
    #         logger.info(f"Processed {len(orders)} orders. Total processed: {total_processed}. Next cursor: {end_cursor}")
    #     else:
    #         update_sync_state(
    #             "order_fetch_job", 
    #             last_cursor=end_cursor, 
    #             is_completed=True,
    #             total_processed=total_processed
    #         )
    #         logger.info(f"Order sync completed. Processed {total_processed} orders in total.")
        
    # except Exception as e:
    #     logger.error(f"Error in scheduled order fetch: {str(e)}")
    #     logger.error(traceback.format_exc())

# Create and configure the scheduler
scheduler = BackgroundScheduler()

# Add the job to run every 2 minutes
scheduler.add_job(
    fetch_and_store_orders,
    'interval',
     minutes=0.5,
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
        # fetch_and_store_orders()
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")
        logger.error(traceback.format_exc())

def shutdown_scheduler():
    """Shutdown the scheduler"""
    scheduler.shutdown()
    logger.info("Scheduler shut down successfully")