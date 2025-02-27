from abc import ABC, abstractmethod
import requests
import bcrypt
from enum import Enum

# Enums
class UserType(Enum):
    LEGAL_ENTITY = "LEGAL_ENTITY"
    NATURAL_PERSON = "NATURAL_PERSON"
    ADMIN = "ADMIN"
    DEFAULT = "DEFAULT"

class ProductStatus(Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"
    PAUSED = "PAUSED"
    CREATED = "CREATED"
    DELETED = "DELETED"

class ProductCategory(Enum):
    REAL_ESTATE = "REAL_ESTATE"
    CARS_AND_PARTS = "CARS_AND_PARTS"
    HOME_DECORATION_AND_UTENSILS = "HOME_DECORATION_AND_UTENSILS"
    CONSTRUCTION_MATERIALS_AND_GARDEN = "CONSTRUCTION_MATERIALS_AND_GARDEN"
    ELECTRONICS_AND_CELL_PHONES = "ELECTRONICS_AND_CELL_PHONES"
    FASHION_AND_BEAUTY = "FASHION_AND_BEAUTY"
    SPORTS_AND_LEISURE = "SPORTS_AND_LEISURE"
    AGRICULTURE_AND_INDUSTRY = "AGRICULTURE_AND_INDUSTRY"
    SERVICES = "SERVICES"
    JOBS = "JOBS"
    BABY_ITEMS = "BABY_ITEMS"
    PETS = "PETS"
    MUSIC_AND_HOBBIES = "MUSIC_AND_HOBBIES"
    DEFALUT = "DEFAULT"

# Observer classes
class UserObserver:
    def __init__(self, user):
        self.user = user

    def update(self, product):
        print(f"Olá {self.user.user_name}, o produto '{product.name}' agora está disponível!")

class ProductObservable:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, product):
        for observer in self._observers:
            observer.update(product)

# Classe de Produto
class Product(ProductObservable):
    id_counter = 1

    def __init__(self, name: str, price: float, description: str, category: ProductCategory = ProductCategory.DEFALUT, status: ProductStatus = ProductStatus.CREATED):
        super().__init__()
        self.id = Product.id_counter
        Product.id_counter += 1
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.status = status

    def update_status(self, new_status: ProductStatus):
        self.status = new_status
        print(f"Status do produto '{self.name}' atualizado para {self.status.value}.")
        if new_status == ProductStatus.AVAILABLE:
            self.notify_observers(self)

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"Nome: {self.name}\n"
                f"Preço: R${self.price:.2f}\n"
                f"Descrição: {self.description}\n"
                f"Categoria: {self.category.name}\n"
                f"Status: {self.status.name}")

# Classe para obter dados da localização via CEP
class Location:
    def __init__(self, cep):
        self.cep = cep
        self.data = None
    
    def fetch_data(self):
        formatted_cep = self.cep.replace("-", "").strip()
        url = f"https://viacep.com.br/ws/{formatted_cep}/json/"
        response = requests.get(url)
        
        if response.status_code == 200:
            self.data = response.json()
            if "error" in self.data:
                raise ValueError("CEP não encontrado")
        else:
            raise Exception("Erro na requisição da API")
    
    def get_address(self):
        # Sempre retorna um dicionário
        if not self.data:
            return {
                "cep": "Informação não disponível",
                "logradouro": "Informação não disponível",
                "bairro": "Informação não disponível",
                "cidade": "Informação não disponível",
                "estado": "Informação não disponível"
            }
        return {
            "cep": self.data.get("cep"),
            "logradouro": self.data.get("logradouro"),
            "bairro": self.data.get("bairro"),
            "cidade": self.data.get("localidade"),
            "estado": self.data.get("uf")
        }
    
    def __str__(self):
        address = self.get_address()
        return (f"CEP: {self.cep}\n"
                f"Logradouro: {address.get('logradouro', 'N/A')}\n"
                f"Bairro: {address.get('bairro', 'N/A')}\n"
                f"Cidade: {address.get('cidade', 'N/A')}\n"
                f"Estado: {address.get('estado', 'N/A')}")



# Classes de Usuários
class Users(ABC):
    id_counter = 1

    def __init__(self, name: str, user_name: str, password: str, email: str, vat: int, age: int, postal_code: str):
        self.id: int = Users.id_counter
        Users.id_counter += 1
        self.name: str = name
        self.user_name: str = user_name
        self.email: str = email
        self.password: bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.vat: int = vat
        self.age: int = age
        self.location: Location = Location(postal_code)
        self.purchased_products: list[Product] = []
        self.cart: list[Product] = []
        self.wishlist: list[Product] = []
        self.my_products: list[Product] = []
        self.observer = UserObserver(self)

    def restock_product(self, product: Product):
        product.update_status(ProductStatus.AVAILABLE)

    def validate_vat(self):
        vat_length = len(str(self.vat))
        if self.user_type == UserType.NATURAL_PERSON and vat_length != 11:
            raise ValueError("O CPF deve ter exatamente 11 dígitos.")
        if self.user_type == UserType.LEGAL_ENTITY and vat_length != 14:
            raise ValueError("O CNPJ deve ter exatamente 14 dígitos.")

    def authenticate(self, user_name, password):
        return self.user_name == user_name and bcrypt.checkpw(password.encode('utf-8'), self.password)
    
    @staticmethod
    def validate_email(email):
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Email inválido.")

    @staticmethod
    def validate_password(password):
        if len(password) < 6:
            raise ValueError("A senha deve conter ao menos 6 caracteres.")

    def add_product(self, product: Product):
        if product not in self.my_products:
            self.my_products.append(product)
            print(f"Produto {product.name} adicionado com sucesso.")
        else:
            print("Este produto já foi adicionado.")

    def remove_product(self, product: Product):
        if product in self.my_products:
            self.my_products.remove(product)
            print(f"Produto {product.name} removido com sucesso.")
        else:
            print("Este produto não está na sua lista.")

    def edit_product(self, product: Product, name: str = None, price: float = None, 
                     description: str = None, category: ProductCategory = None):
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
        if product not in self.cart:
            self.cart.append(product)
            print(f"Produto {product.name} adicionado ao carrinho.")
        else:
            print("Este produto já está no carrinho.")

    def get_cart_total(self):
        total = sum(product.price for product in self.cart)
        return total

    def view_cart(self):
        if not self.cart:
            print("Seu carrinho está vazio.")
        else:
            print("Produtos no carrinho:")
            for product in self.cart:
                print(f"- {product.name} - R${product.price:.2f}")

    def remove_from_cart(self, product: Product):
        if product in self.cart:
            self.cart.remove(product)
            print(f"Produto {product.name} removido do carrinho.")
        else:
            print("Este produto não está no carrinho.")

    def add_to_wishlist(self, product: Product):
        if product not in self.wishlist:
            self.wishlist.append(product)
            product.register(self.observer)  # registra o observer do usuário
            print(f"Produto {product.name} adicionado à lista de desejos.")
        else:
            print("Este produto já está na lista de desejos.")

    def remove_from_wishlist(self, product: Product):
        if product in self.wishlist:
            self.wishlist.remove(product)
            product.unregister(self.observer)
            print(f"Produto {product.name} removido da lista de desejos.")
        else:
            print("Este produto não está na lista de desejos.")

    def purchase_product(self, product: Product):
        if product in self.cart:
            self.cart.remove(product)
            self.purchased_products.append(product)
            print(f"Produto {product.name} comprado com sucesso.")
        else:
            print("Produto não encontrado no carrinho.")

    def checkout(self):
        if not self.cart:
            print("Seu carrinho está vazio.")
            return
        total = sum(product.price for product in self.cart)
        print(f"Valor total: R${total:.2f}")
        self.purchased_products.extend(self.cart)
        self.cart.clear()
        print("Compra realizada com sucesso. Produtos comprados:")
        for product in self.purchased_products:
            print(f"- {product.name}")

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"Nome: {self.name}\n"
                f"Usuário: {self.user_name}\n"
                f"Email: {self.email}\n"
                f"Idade: {self.age}\n"
                f"CPF/CNPJ: {self.vat}\n"
                f"Localização: {self.location}\n"
                f"Tipo de usuário: {self.user_type}")


class LegalEntity(Users):
    def __init__(self, name, user_name, password, email, vat, age, postal_code):
        super().__init__(name, user_name, password, email, vat, age, postal_code)
        self.user_type = UserType.LEGAL_ENTITY

class NaturalPerson(Users):
    def __init__(self, name, user_name, password, email, vat, age, postal_code):
        super().__init__(name, user_name, password, email, vat, age, postal_code)
        self.user_type = UserType.NATURAL_PERSON

class UserFactory:
    @staticmethod
    def create_user(user_type, *args):
        if user_type == UserType.NATURAL_PERSON:
            return NaturalPerson(*args)
        elif user_type == UserType.LEGAL_ENTITY:
            return LegalEntity(*args)
        else:
            raise ValueError("Invalid UserType")