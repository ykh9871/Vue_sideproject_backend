from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class Product(BaseModel):
    id: int
    product_name: str
    description: str
    price: Decimal
    imgurl: str
    category_name: str
    created_at: Optional[datetime]