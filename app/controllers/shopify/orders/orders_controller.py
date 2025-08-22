from app.services.shopify_client import query_shopify

def fetch_orders(first: int = 10, status: str = "status:any"):
    query = f"""
    {{
      orders(first: {first}, query: "{status}") {{
        edges {{
          cursor
          node {{
            id
            name
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
    return data["orders"]
