from pydantic import BaseModel

class OrderNode(BaseModel):
    id: str
    name: str
