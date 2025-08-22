from pydantic import BaseModel

class Money(BaseModel):
    amount: str
    currencyCode: str

class TotalPriceSet(BaseModel):
    shopMoney: Money

class OrderResponse(BaseModel):
    id: str
    name: str
    email: str | None
    createdAt: str
    totalPriceSet: TotalPriceSet
