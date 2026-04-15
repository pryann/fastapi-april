from typing import Literal

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str
    quantity: int


class ItemCreate(BaseModel):
    name: str
    quantity: int


class ItemPartialUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None


class ItemQuery(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(10, gt=0)
    order_by: Literal["id", "quantity"] = "id"
