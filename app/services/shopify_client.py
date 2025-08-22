import requests
from app.config import SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN

def query_shopify(query: str):
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }

    response = requests.post(SHOPIFY_STORE_URL, headers=headers, json={"query": query})

    if response.status_code != 200:
        raise Exception(f"Shopify API error: {response.status_code} - {response.text}")

    data = response.json()
    if "errors" in data:
        raise Exception(f"Shopify GraphQL errors: {data['errors']}")

    return data.get("data")
