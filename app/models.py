from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    in_stock: bool = True


class Item(ItemCreate):
    id: int


class ItemError(BaseModel):
    details: str
