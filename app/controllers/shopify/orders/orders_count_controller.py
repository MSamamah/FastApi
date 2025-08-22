from app.services.shopify_client import query_shopify

def fetch_orders_count():
    query = """
    query OrdersCount {
      ordersCount(limit: 2000) {
        count
        precision
      }
    }
    """
    
    # Execute the query
    data = query_shopify(query)
    
    # Extract the ordersCount from the response
    # The response structure should be: {"data": {"ordersCount": {"count": X, "precision": "EXACT"}}}
    if "data" in data and "ordersCount" in data["data"]:
        return data["data"]["ordersCount"]
    else:
        # Fallback to manual counting if ordersCount isn't available
        fallback_query = """
        {
          orders(first: 250) {
            edges {
              node {
                id
              }
            }
          }
        }
        """
        fallback_data = query_shopify(fallback_query)
        
        # Extract edges from the response
        if "data" in fallback_data and "orders" in fallback_data["data"]:
            edges = fallback_data["data"]["orders"]["edges"]
        else:
            edges = fallback_data.get("orders", {}).get("edges", [])
            
        return {"count": len(edges), "precision": "ESTIMATED"}