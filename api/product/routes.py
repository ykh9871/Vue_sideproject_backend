from fastapi import APIRouter
from app.product.dto.dto import Product
from app.product.service.service import ProductService
from app.product.repository.repository import ProductRepository
from typing import List, Optional

router = APIRouter()

product_service = ProductService()
product_repository = ProductRepository()

@router.get("/product/", response_model=List[Product])
async def get_all_products(name: Optional[str] = None):
    return product_service.get_all_products(name)
    