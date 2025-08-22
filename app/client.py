import requests
from constants.constants import BASE_URL

def get_orders():
    response = requests.get(f"{BASE_URL}/shopify/orders?limit=5")
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    get_orders()
