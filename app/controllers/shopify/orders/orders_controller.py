from app.services.shopify_client import query_shopify

def fetch_orders(first: int = 10, after: str = None, status: str = "status:any"):
    """
    Fetch Shopify orders with optional limit, cursor, and status filter.
    Uses a simplified query based on the Shopify API documentation.
    """
    after_clause = f', after: "{after}"' if after else ''
    
    query = f"""
    {{
      orders(first: {first}, query: "{status}"{after_clause}) {{
        edges {{
          cursor
          node {{
            id
            name
            email
            createdAt
            totalPriceSet {{
              shopMoney {{
                amount
                currencyCode
              }}
            }}
          }}
        }}
        pageInfo {{
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }}
      }}
    }}
    """

    data = query_shopify(query)
    return data["orders"] if data else {"edges": [], "pageInfo": {}}

def fetch_all_orders(status: str = "status:any", batch_size: int = 100):
    """
    Fetch all orders using cursor-based pagination.
    Returns a generator that yields batches of orders.
    """
    has_next_page = True
    after_cursor = None
    
    while has_next_page:
        orders_data = fetch_orders(first=batch_size, after=after_cursor, status=status)
        
        # Extract orders and page info
        orders = orders_data.get('edges', [])
        page_info = orders_data.get('pageInfo', {})
        
        # Yield the current batch of orders
        if orders:
            yield orders
        
        # Check if there are more pages
        has_next_page = page_info.get('hasNextPage', False)
        after_cursor = page_info.get('endCursor')