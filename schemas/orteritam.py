from pydantic import BaseModel
from typing import Optional

class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class OrderItemUpdate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float

class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float    


