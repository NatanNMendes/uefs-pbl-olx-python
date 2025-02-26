import time
import bcrypt
from models.users import Users
from models.natural_person import NaturalPerson
from models.legal_entity import LegalEntity
from controllers.ProductController import ProductController
from controllers.PurchaseController import PurchaseController
from views.MarketplaceView import MarketplaceView
from views.AccountView import AccountView
from views.ProductView import ProductView
from utils.users_enum import UserType

class MarketplaceApp:
    def __init__(self):
        self.users = []
        self.current_user = None
        self.product_controller = ProductController()
        self.purchase_controller = PurchaseController()

    def run(self):
        while True:
            choice = MarketplaceView.menu_principal()
            if choice == 'criar_conta':
                self.create_account()
            elif choice == 'fazer_login':
                self.login()
            elif choice == 'sair':
                print("Saindo do sistema...")
                break

    def create_account(self):
        nome, email, senha = AccountView.criar_conta()
        user_type = input("Digite '1' para Pessoa Física ou '2' para Pessoa Jurídica: ")
        senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        if user_type == '1':
            user = NaturalPerson(nome, email, senha_hashed, 30, "12345-678")
        elif user_type == '2':
            user = LegalEntity(nome, email, senha_hashed, 12345678000199, 30, "12345-678")
        else:
            print("Opção inválida!")
            return
        self.users.append(user)
        MarketplaceView.exibir_mensagem_sucesso("Conta criada com sucesso!")

    def login(self):
        email, senha = AccountView.fazer_login()
        for user in self.users:
            if user.email == email and bcrypt.checkpw(senha.encode('utf-8'), user.password):
                self.current_user = user
                print(f"Bem-vindo, {user.name}!")
                self.main_menu()
                return
        MarketplaceView.exibir_mensagem_erro("Email ou senha incorretos!")

    def main_menu(self):
        while True:
            choice = MarketplaceView.menu_opcoes()
            if choice == '1':
                self.buy_product()
            elif choice == '2':
                self.add_product()
            elif choice == '3':
                self.remove_product()
            elif choice == '4':
                print("Saindo...")
                self.current_user = None
                break

    def buy_product(self):
        products = self.product_controller.products
        ProductView.exibir_produtos(products)
        if products:
            product_id = int(input("Digite o ID do produto que deseja comprar: "))
            product = next((p for p in products if p.id == product_id), None)
            if product:
                self.purchase_controller.checkout(self.current_user)
                print("Compra realizada com sucesso!")
            else:
                print("Produto não encontrado.")

    def add_product(self):
        nome, descricao, preco, categoria = ProductView.cadastrar_produto()
        new_product = Product(nome, descricao, preco, categoria)
        self.product_controller.add_product(self.current_user, new_product)
        print("Produto cadastrado com sucesso!")

    def remove_product(self):
        product_id = ProductView.remover_produto(self.product_controller.products)
        product = next((p for p in self.product_controller.products if p.id == product_id), None)
        if product:
            self.product_controller.remove_product(self.current_user, product)
            print("Produto removido com sucesso!")
        else:
            print("Produto não encontrado!")

if __name__ == "__main__":
    app = MarketplaceApp()
    app.run()

