from typing import Annotated, List, Optional
from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=200)]
    description: Annotated[str, Field(min_length=1, max_length=500)]
    category: Annotated[str, Field(min_length=1, max_length=100)]
    brand: Annotated[str, Field(min_length=1, max_length=100)]
    price: Annotated[float, Field(ge=0.01)]
    quantity: Annotated[int, Field(ge=0)]


class ProductListSchema(BaseModel):
    products: List[ProductSchema]


class FutureStockEventSchema(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=120)]
    event_type: Annotated[str, Field(min_length=3, max_length=50)]
    expected_date: str
    product_name: Annotated[str, Field(min_length=1, max_length=100)]
    quantity_change: int
    note: Optional[str] = None


class FutureStockEventListSchema(BaseModel):
    events: List[FutureStockEventSchema]
