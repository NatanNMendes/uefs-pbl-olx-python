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

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, category={self.category}, status={self.status})"

    def update_status(self, status: ProductStatus):
        """Atualiza o status do produto (ex: vendido, indisponível)"""
        self.status = status
        print(f"O status do produto {self.name} foi atualizado para {status}.")

    def update_price(self, price: float):
        """Atualiza o preço do produto"""
        self.price = price
        print(f"O preço do produto {self.name} foi atualizado para R${self.price:.2f}.")

    def update_description(self, description: str):
        """Atualiza a descrição do produto"""
        self.description = description
        print(f"A descrição do produto {self.name} foi atualizada.")

    def is_available(self):
        """Verifica se o produto está disponível para venda"""
        return self.status == ProductStatus.AVAILABLE

    def sell_product(self):
        """Vende o produto, alterando seu status para 'Vendido'"""
        if self.is_available():
            self.update_status(ProductStatus.SOLD)
            print(f"Produto {self.name} vendido com sucesso!")
        else:
            print(f"Produto {self.name} não está disponível para venda.")

    def __str__(self):
        return (f"\n[PRODUTO CADASTRADO]\n"
                f"ID: {self.id}\n"
                f"Nome: {self.name}\n"
                f"Descrição: {self.description}\n"
                f"Preço: R$ {self.price:.2f}\n"
                f"Categoria: {self.category.value}\n"
                f"Status: {self.status.value}\n"
                f"Criado em: {self.created_at.strftime('%d/%m/%Y %H:%M:%S')}\n")
