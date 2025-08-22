from pydantic import BaseModel

class OrdersCountResponse(BaseModel):
    count: int
