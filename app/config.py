import os
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

if not SHOPIFY_STORE_URL or not SHOPIFY_ACCESS_TOKEN:
    raise ValueError("Missing SHOPIFY credentials in .env file")
