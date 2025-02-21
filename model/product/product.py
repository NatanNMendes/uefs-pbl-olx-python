from abc import ABC, abstractmethod
from datetime import datetime
from utils.product_enum import *

class Product(ABC):
    id_counter = 1

    def __init__(self, name, description, price):
        self.id = Product.id_counter
        Product.id_counter += 1
        self.name = name
        self.description = description
        self.status = ProductStatus.AVAILABLE
        self.category = ProductCategory.REAL_ESTATE
        self.created_at = datetime.now()
        self.price = price
