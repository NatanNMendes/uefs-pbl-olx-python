from abc import ABC, abstractmethod
from utils.users_enum import *
from utils.location import Location
from product.product import Product
from product.utils.product_enum import ProductCategory

class Users(ABC):
    id_counter = 1

    def __init__(self, name: str, user_name: str, email: str, vat: int, age: int, postal_code: str):
        self.id: int = Users.id_counter
        Users.id_counter += 1
        self.name: str = name
        self.user_name: str = user_name
        self.email: str = email
        self.vat: int = vat
        self.age: int = age
        self.location: Location = Location(postal_code) 
        self.purchased_products: list[Product] = []
        self.cart: list[Product] = []
        self.wishlist: list[Product] = []
        self.my_products: list[Product] = []

    def validate_vat(self):
        vat_length = len(str(self.vat))
        
        if self.user_type == UserType.NATURAL_PERSON and vat_length != 11:
            raise ValueError("O CPF deve ter exatamente 11 dígitos.")
        
        if self.user_type == UserType.LEGAL_ENTITY and vat_length != 14:
            raise ValueError("O CNPJ deve ter exatamente 14 dígitos.")

    def add_product(self, product: Product):
        """Adiciona um produto à lista de produtos do usuário"""
        if product not in self.my_products:
            self.my_products.append(product)
            print(f"Produto {product.name} adicionado com sucesso.")
        else:
            print("Este produto já foi adicionado.")

    def remove_product(self, product: Product):
        """Remove um produto da lista de produtos do usuário"""
        if product in self.my_products:
            self.my_products.remove(product)
            print(f"Produto {product.name} removido com sucesso.")
        else:
            print("Este produto não está na sua lista.")

    def edit_product(self, product: Product, name: str = None, price: float = None, 
                 description: str = None, category: ProductCategory = None):
        """Edita todas as informações de um produto se ele for criado pelo usuário"""
        if product in self.my_products:
            if name:
                product.name = name
            if price:
                product.price = price
            if description:
                product.description = description
            if category:
                product.category = category
            
            print(f"Produto '{product.name}' atualizado com sucesso.")
        else:
            print("Você não tem permissão para editar este produto.")


    def add_to_cart(self, product: Product):
        """Adiciona um produto ao carrinho"""
        if product not in self.cart:
            self.cart.append(product)
            print(f"Produto {product.name} adicionado ao carrinho.")
        else:
            print("Este produto já está no carrinho.")

    def remove_from_cart(self, product: Product):
        """Remove um produto do carrinho"""
        if product in self.cart:
            self.cart.remove(product)
            print(f"Produto {product.name} removido do carrinho.")
        else:
            print("Este produto não está no carrinho.")

    def add_to_wishlist(self, product: Product):
        """Adiciona um produto à lista de desejos"""
        if product not in self.wishlist:
            self.wishlist.append(product)
            print(f"Produto {product.name} adicionado à lista de desejos.")
        else:
            print("Este produto já está na lista de desejos.")

    def remove_from_wishlist(self, product: Product):
        """Remove um produto da lista de desejos"""
        if product in self.wishlist:
            self.wishlist.remove(product)
            print(f"Produto {product.name} removido da lista de desejos.")
        else:
            print("Este produto não está na lista de desejos.")

