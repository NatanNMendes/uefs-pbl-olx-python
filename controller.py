from view import View
from model import UserType, Product, Users, ProductStatus, Location

class Controller:
    def __init__(self):
        self.users = []      # Lista de usuários registrados
        self.products = []   # Lista global de produtos
        self.current_user = None

    def run(self):
        while True:
            if not self.current_user:
                options = {
                    "1": "Registrar Usuário",
                    "2": "Login",
                    "3": "Sair"
                }
                View.display_menu("Menu Inicial", options)
                choice = View.get_input("Escolha uma opção: ")
                if choice == "1":
                    self.register_user()
                elif choice == "2":
                    self.login()
                elif choice == "3":
                    View.display_message("Encerrando a aplicação.")
                    break
                else:
                    View.display_message("Opção inválida!")
            else:
                while self.current_user:
                    self.user_menu()

    def display_notifications(self):
        # Exibe as notificações armazenadas no usuário atual, se houver.
        # É necessário que o objeto usuário tenha o atributo "notifications" (uma lista).
        if hasattr(self.current_user, "notifications") and self.current_user.notifications:
            View.display_message("\n--- Notificações ---")
            for notification in self.current_user.notifications:
                View.display_message(notification)
            # Após exibir, limpa as notificações.
            self.current_user.notifications.clear()

    def register_user(self):
        View.display_message("\n--- Registro de Usuário ---")
        name = View.get_input("Nome: ")
        user_name = View.get_input("Nome de usuário: ")
        password = View.get_input("Senha: ")
        email = View.get_input("Email: ")
        vat = View.get_input("CPF (11 dígitos) ou CNPJ (14 dígitos): ")
        age = View.get_input("Idade: ")
        postal_code = View.get_input("CEP: ")

        # Define o tipo de usuário automaticamente
        if len(vat) == 11:
            user_type = UserType.NATURAL_PERSON
            View.display_message("Tipo de usuário: Pessoa Física")
        elif len(vat) == 14:
            user_type = UserType.LEGAL_ENTITY
            View.display_message("Tipo de usuário: Pessoa Jurídica")
        else:
            View.display_message("Número de CPF ou CNPJ inválido. Registro cancelado.")
            return

        try:
            user = Users(name, user_name, password, email, int(vat), int(age), postal_code)
            user.user_type = user_type
            # Adiciona uma lista de notificações para o usuário
            user.notifications = []
            user.location.fetch_data()
            user.validate_vat()

            self.users.append(user)
            View.display_message("Usuário registrado com sucesso!")
            print(user)
        except ValueError as e:
            View.display_message(f"Erro: {e}")
        except Exception as e:
            View.display_message(f"Ocorreu um erro: {e}")

    def login(self):
        View.display_message("\n--- Login ---")
        user_name = View.get_input("Nome de usuário: ")
        password = View.get_input("Senha: ")
        
        found = False
        for user in self.users:
            if user.authenticate(user_name, password):
                self.current_user = user
                # Certifica-se de que o usuário possui o atributo de notificações
                if not hasattr(self.current_user, "notifications"):
                    self.current_user.notifications = []
                found = True
                break
        if found:
            View.display_message(f"Login bem-sucedido. Bem-vindo(a), {self.current_user.user_name}!")
        else:
            View.display_message("Usuário ou senha incorretos.")
        View.pause()

    def user_menu(self):
        # Exibe as notificações (se houver) antes do menu de usuário
        self.display_notifications()

        options = {
            "1": "Adicionar Produto",
            "2": "Listar Produtos",
            "3": "Adicionar Produto ao Carrinho",
            "4": "Visualizar Carrinho",
            "5": "Remover Produto do Carrinho",
            "6": "Checkout",
            "7": "Adicionar Produto à Wishlist",
            "8": "Editar Produto",
            "9": "Remover Produto (meus produtos)",
            "10": "Logout",
            "11": "Restocar Produto"  # Nova opção para restocar e notificar
        }
        View.display_menu("Menu do Usuário", options)
        choice = View.get_input("Escolha uma opção: ")
        if choice == "1":
            self.add_product()
        elif choice == "2":
            self.list_products()
        elif choice == "3":
            self.add_product_to_cart()
        elif choice == "4":
            self.view_cart()
        elif choice == "5":
            self.remove_product_from_cart()
        elif choice == "6":
            self.checkout()
        elif choice == "7":
            self.add_to_wishlist()
        elif choice == "8":
            self.edit_product()
        elif choice == "9":
            self.remove_user_product()
        elif choice == "10":
            self.logout()
        elif choice == "11":
            self.restock_product()
        else:
            View.display_message("Opção inválida!")
        View.pause()

    def add_product(self):
        View.display_message("\n--- Adicionar Produto ---")
        name = View.get_input("Nome do produto: ")
        description = View.get_input("Descrição do produto: ")
        price_input = View.get_input("Preço do produto: ")
        try:
            price = float(price_input)
        except ValueError:
            View.display_message("Preço inválido!")
            return
        
        product = Product(name, description, price)
        self.products.append(product)
        self.current_user.add_product(product)
        View.display_message("Produto adicionado com sucesso!")

    def list_products(self):
        View.display_message("\n--- Lista de Produtos ---")
        if not self.products:
            View.display_message("Nenhum produto cadastrado.")
        else:
            for product in self.products:
                View.display_message(str(product))

    def add_product_to_cart(self):
        View.display_message("\n--- Adicionar Produto ao Carrinho ---")
        product_id = View.get_input("Digite o ID do produto: ")
        try:
            product_id = int(product_id)
        except ValueError:
            View.display_message("ID inválido!")
            return
        
        product = next((p for p in self.products if p.id == product_id), None)
        if product:
            self.current_user.add_to_cart(product)
        else:
            View.display_message("Produto não encontrado.")

    def view_cart(self):
        View.display_message("\n--- Carrinho de Compras ---")
        self.current_user.view_cart()

    def remove_product_from_cart(self):
        View.display_message("\n--- Remover Produto do Carrinho ---")
        product_id = View.get_input("Digite o ID do produto a remover: ")
        try:
            product_id = int(product_id)
        except ValueError:
            View.display_message("ID inválido!")
            return
        
        product = next((p for p in self.current_user.cart if p.id == product_id), None)
        if product:
            self.current_user.remove_from_cart(product)
        else:
            View.display_message("Produto não encontrado no carrinho.")

    def checkout(self):
        View.display_message("\n--- Checkout ---")
        self.current_user.checkout()

    def add_to_wishlist(self):
        View.display_message("\n--- Adicionar Produto à Wishlist ---")
        product_id = View.get_input("Digite o ID do produto: ")
        try:
            product_id = int(product_id)
        except ValueError:
            View.display_message("ID inválido!")
            return
        
        product = next((p for p in self.products if p.id == product_id), None)
        if product:
            self.current_user.add_to_wishlist(product)
        else:
            View.display_message("Produto não encontrado.")

    def edit_product(self):
        View.display_message("\n--- Editar Produto ---")
        if not self.current_user.my_products:
            View.display_message("Você não tem produtos cadastrados.")
            return
        View.display_message("Seus produtos:")
        for product in self.current_user.my_products:
            View.display_message(str(product))
        product_id = View.get_input("Digite o ID do produto a editar: ")
        try:
            product_id = int(product_id)
        except ValueError:
            View.display_message("ID inválido!")
            return
        
        product = next((p for p in self.current_user.my_products if p.id == product_id), None)
        if not product:
            View.display_message("Produto não encontrado.")
            return
        
        new_name = View.get_input("Novo nome (deixe em branco para não alterar): ")
        new_price_input = View.get_input("Novo preço (deixe em branco para não alterar): ")
        new_description = View.get_input("Nova descrição (deixe em branco para não alterar): ")
        new_price = None
        if new_price_input.strip():
            try:
                new_price = float(new_price_input)
            except ValueError:
                View.display_message("Preço inválido!")
                return
        self.current_user.edit_product(
            product,
            name=new_name if new_name.strip() else None,
            price=new_price,
            description=new_description if new_description.strip() else None
        )
        View.display_message("Produto atualizado.")

    def remove_user_product(self):
        View.display_message("\n--- Remover Produto (Meus Produtos) ---")
        if not self.current_user.my_products:
            View.display_message("Você não tem produtos cadastrados.")
            return
        View.display_message("Seus produtos:")
        for product in self.current_user.my_products:
            View.display_message(str(product))
        product_id = View.get_input("Digite o ID do produto a remover: ")
        try:
            product_id = int(product_id)
        except ValueError:
            View.display_message("ID inválido!")
            return
        
        product = next((p for p in self.current_user.my_products if p.id == product_id), None)
        if product:
            self.current_user.remove_product(product)
            if product in self.products:
                self.products.remove(product)
            View.display_message("Produto removido com sucesso.")
        else:
            View.display_message("Produto não encontrado.")

    def restock_product(self):
        View.display_message("\n--- Restocar Produto ---")
        if not self.current_user.my_products:
            View.display_message("Você não tem produtos cadastrados para restocar.")
            return
        
        View.display_message("Seus produtos:")
        for product in self.current_user.my_products:
            View.display_message(str(product))
        
        product_id = View.get_input("Digite o ID do produto que deseja restocar: ")
        try:
            product_id = int(product_id)
        except ValueError:
            View.display_message("ID inválido!")
            return
        
        product = next((p for p in self.current_user.my_products if p.id == product_id), None)
        if product:
            if product.status != ProductStatus.AVAILABLE:
                product.update_status(ProductStatus.AVAILABLE)
                View.display_message("Produto restocado e notificação enviada aos interessados!")
            else:
                View.display_message("O produto já está disponível.")
        else:
            View.display_message("Produto não encontrado.")

    def logout(self):
        View.display_message(f"Usuário {self.current_user.user_name} deslogado.")
        self.current_user = None

if __name__ == "__main__":
    controller = Controller()
    controller.run()
