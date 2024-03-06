from app.product.dto.dto import Product
from app.product.repository.repository import ProductRepository
from fastapi import HTTPException
from typing import List, Optional

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def get_all_products(self, name:Optional[str] = None):
        products = self.product_repository.get_all_products(name)
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return products