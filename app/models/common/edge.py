from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class Edge(BaseModel, Generic[T]):
    cursor: str
    node: T
