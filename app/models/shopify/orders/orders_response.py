from typing import List
from pydantic import BaseModel
from app.models.common.page_info import PageInfo
from app.models.common.edge import Edge
from app.models.shopify.orders.order_node import OrderNode

class OrdersResponse(BaseModel):
    edges: List[Edge[OrderNode]]
    pageInfo: PageInfo
