from app.product.dto.dto import Product
from datetime import datetime
from typing import List, Optional
import mysql.connector

class ProductRepository:
    def __init__(self):
        self.conn = mysql.connector.connect(
            port=3307,
            user="root",
            host="localhost",
            password="ykh9871",
            database="shoppingmall"
        )
        self.cursor= self.conn.cursor()

    def get_all_products(self, name: Optional[str] = None):
        if name:
            self.cursor.execute(
                "SELECT p.ProductID, p.Name AS ProductName, p.Description, p.Price, p.Imgurl, c.Name AS CategoryName, p.CreatedAt "
                "FROM Product p "
                "JOIN ProductCategory pc ON p.ProductID = pc.ProductID "
                "JOIN Category c ON pc.CategoryID = c.CategoryID "
                "WHERE p.Name LIKE %s",
                ('%' + name + '%',)
            )
        else:
            self.cursor.execute(
                "SELECT p.ProductID, p.Name AS ProductName, p.Description, p.Price, p.Imgurl, c.Name AS CategoryName, p.CreatedAt "
                "FROM Product p "
                "JOIN ProductCategory pc ON p.ProductID = pc.ProductID "
                "JOIN Category c ON pc.CategoryID = c.CategoryID"
            )
        products = []
        for row in self.cursor.fetchall():
            product = {
                'id': row[0],
                'product_name': row[1],
                'description': row[2],
                'price': row[3],
                'imgurl': row[4],
                'category_name': row[5],
                'created_at': row[6]
            }
            products.append(product)
        return products
