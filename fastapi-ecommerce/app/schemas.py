from pydantic import BaseModel, EmailStr
from typing import List, Optional


# ---------------------------
# Customers
# ---------------------------
class CustomerCreate(BaseModel):
    name: str
    email: str


class CustomerRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


# ---------------------------
# Products
# ---------------------------
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    class Config:
        from_attributes = True


# ---------------------------
# Categories
# ---------------------------
class CategoryCreate(BaseModel):
    name: str


class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# ---------------------------
# Orders
# ---------------------------
class OrderCreate(BaseModel):
    customer_id: int


class OrderRead(BaseModel):
    id: int
    customer_id: int

    class Config:
        from_attributes = True


# ---------------------------
# Order Items
# ---------------------------
class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItemRead(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
