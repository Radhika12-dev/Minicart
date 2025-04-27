from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime

class CreateCustomer(BaseModel):
    name: str 
    email: EmailStr
    phone: str  
    address: str  

class CreateProducts(BaseModel):
    name: str 
    description: str 
    price: float

class CreateOrder(BaseModel):
    customer_id: int 
    order_date: datetime = Field(default_factory=datetime.utcnow)
    total_amount: float
    products: List[int]  # List of product IDs

class ProductOut(BaseModel):
    id: int 
    name: str 
    description: str 
    price: float

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models directly

class OrderOut(BaseModel):
    id: int 
    customer_id: int 
    order_date: datetime
    total_amount: float
    products: List[ProductOut]  # List of product IDs

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models directly