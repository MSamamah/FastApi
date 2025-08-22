from app.services.shopify_client import query_shopify

def fetch_order_by_id(order_id: str):
    query = f"""
    query {{
      order(id: "gid://shopify/Order/{order_id}") {{
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
    """
    data = query_shopify(query)
    return data["order"]
