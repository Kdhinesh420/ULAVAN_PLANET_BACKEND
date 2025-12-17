from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    product_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    class Config:
        from_attributes = True
