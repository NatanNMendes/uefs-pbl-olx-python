from view import View
from model import UserType, Product, Users, ProductStatus, ProductCategory

class Controller:
    def __init__(self):
        self.users = [] 
        self.products = []
        self.current_user = None

    def find_product_by_name(self, search_term):
        return [product for product in self.products if search_term.lower() in product.name.lower()]
    
    def find_product_by_category(self, search_term):
        return [product for product in self.products if search_term.lower() in product.category.value.lower()]


    def display_banner(self):
        banner = r"""
                              @@@@@@@                                   
                              @@@@@@@@                                  
                              @@@@@@@@                                  
                              @@@@@@@@                                  
        @@@@@@@@@@@           @@@@@@@@           @@               @@    
     @@@@@@@@@@@@@@@@@        @@@@@@@@         @@@@@@           @@@@@@  
   @@@@@@@@@@@@@@@@@@@@@      @@@@@@@@       @@@@@@@@@@       @@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@    @@@@@@@@        @@@@@@@@@@     @@@@@@@@@@ 
 @@@@@@@@@        @@@@@@@@@   @@@@@@@@         @@@@@@@@@@@ @@@@@@@@@@   
@@@@@@@@           @@@@@@@@   @@@@@@@@           @@@@@@@@@@@@@@@@@@@    
@@@@@@@@            @@@@@@@   @@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@      
@@@@@@@             @@@@@@@@  @@@@@@@@@@@@@@@@@@    @@@@@@@@@@@@        
@@@@@@@             @@@@@@@@  @@@@@@@@@@@@@@@@@@     @@@@@@@@@@@        
@@@@@@@@            @@@@@@@@  @@@@@@@@@@@@@@@@@@   @@@@@@@@@@@@@@@      
@@@@@@@@           @@@@@@@@                      @@@@@@@@@@@@@@@@@@@    
 @@@@@@@@@        @@@@@@@@@                    @@@@@@@@@@@ @@@@@@@@@@   
  @@@@@@@@@@@@@@@@@@@@@@@@                    @@@@@@@@@@     @@@@@@@@@@ 
   @@@@@@@@@@@@@@@@@@@@@                    @@@@@@@@@@@       @@@@@@@@@@
     @@@@@@@@@@@@@@@@@                       @@@@@@@@          @@@@@@@@@
       @@@@@@@@@@@@@                           @@@@@             @@@@@  
            """
        
        View.display_message(banner)
        View.display_message("Bem-vindo(a) ao OLX!")
        self.run()

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
        if hasattr(self.current_user, "notifications") and self.current_user.notifications:
            View.display_message("\n--- Notificações ---")
            for notification in self.current_user.notifications:
                View.display_message(notification)
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
        balance = View.get_input("Saldo: ")
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
            user = Users(name, user_name, password, email, int(vat), int(age), postal_code, float(balance))
            user.user_type = user_type
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
            "9": "Remover Produto",
            "10": "Logout",
            "11": "Restocar Produto",
            "12": "Depositar",
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
        elif choice == "12":
            self.deposit()
        else:
            View.display_message("Opção inválida!")
        View.pause()

    def add_product(self):
        View.display_message("\n--- Adicionar Produto ---")
        name = View.get_input("Nome do produto: ")
        description = View.get_input("Descrição do produto: ")
        price_input = View.get_input("Preço do produto: ")
        quantity_input = View.get_input("Quantidade: ")
        
        try:
            price = float(price_input)
            quantity = int(quantity_input)
        except ValueError:
            View.display_message("Preço ou Quantidade inválidos!")
            return

        View.display_message("\nEscolha a categoria do produto:")
        for index, category in enumerate(ProductCategory):
            View.display_message(f"{index + 1}. {category.value}")

        category_choice = View.get_input("Digite o número da categoria: ")

        try:
            category_choice = int(category_choice) - 1
            category = list(ProductCategory)[category_choice]
        except (ValueError, IndexError):
            View.display_message("Categoria inválida!")
            return

        product = Product(name, description, price, quantity, category)
        
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
        search_type = View.get_input("Deseja buscar por nome ou categoria? (Digite 'nome' ou 'categoria'): ").strip().lower()

        if search_type == 'nome':
            search_term = View.get_input("Digite o nome do produto que deseja adicionar ao carrinho: ").strip()
            products = self.find_product_by_name(search_term)
        elif search_type == 'categoria':
            search_term = View.get_input("Digite a categoria do produto que deseja Digite o nome do produto que deseja adicionar ao carrinho:: ").strip()
            products = self.find_product_by_category(search_term)
        else:
            View.display_message("Opção inválida! Escolha 'nome' ou 'categoria'.")
            return
        if not products:
            View.display_message("Nenhum produto encontrado.")
            return
        
        for product in products:
            if product:
                self.current_user.add_to_cart(product)
            else:
                View.display_message("Produto não encontrado.")

    def view_cart(self):
        View.display_message("\n--- Carrinho de Compras ---")
        self.current_user.view_cart()

    def remove_product_from_cart(self):
        View.display_message("\n--- Remover Produto do Carrinho ---")
        
        search_type = View.get_input("Deseja buscar por nome ou categoria? (Digite 'nome' ou 'categoria'): ").strip().lower()

        if search_type == 'nome':
            search_term = View.get_input("Digite o nome do produto que deseja remover do carrinho: ").strip()
            products = self.find_product_by_name(search_term)
        elif search_type == 'categoria':
            search_term = View.get_input("Digite a categoria do produto que deseja remover do carrinho: ").strip()
            products = self.find_product_by_category(search_term)
        else:
            View.display_message("Opção inválida! Escolha 'nome' ou 'categoria'.")
            return

        if not products:
            View.display_message("Nenhum produto encontrado.")
            return
                
        for product in products:
            if product:
                self.current_user.remove_from_cart(product)
            else:
                View.display_message("Produto não encontrado no carrinho.")

    def checkout(self):
        View.display_message("\n--- Checkout ---")

        if not self.current_user.cart:
            View.display_message("O carrinho está vazio. Adicione produtos antes de realizar o checkout.")
            return

        total_price = sum([product.price for product in self.current_user.cart])

        View.display_message(f"Total a pagar: R${total_price:.2f}")

        if self.current_user.balance >= total_price:
            self.current_user.balance -= total_price

            for product in self.current_user.cart:
                self.current_user.purchase_product(product)
                
                if product.quantity <= 0:
                    View.display_message(f"Produto {product.name} esgotado.")
            self.current_user.clear_cart()

            View.display_message(f"Compra realizada com sucesso! Seu novo saldo é R${self.current_user.balance:.2f}")
        else:
            View.display_message("Saldo insuficiente para realizar a compra.")

    
    View.pause()

    def add_to_wishlist(self):
        View.display_message("\n--- Adicionar Produto à Wishlist ---")
        search_type = View.get_input("Deseja buscar por nome ou categoria? (Digite 'nome' ou 'categoria'): ").strip().lower()

        if search_type == 'nome':
            search_term = View.get_input("Digite o nome do produto que deseja adicionar a lista de desejos: ").strip()
            products = self.find_product_by_name(search_term)
        elif search_type == 'categoria':
            search_term = View.get_input("Digite a categoria do produto que deseja deseja adicionar a lista de desejos: ").strip()
            products = self.find_product_by_category(search_term)
        else:
            View.display_message("Opção inválida! Escolha 'nome' ou 'categoria'.")
            return

        if not products:
            View.display_message("Nenhum produto encontrado.")
            return
        
        for product in products:
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
        
        search_type = View.get_input("Deseja buscar por nome ou categoria? (Digite 'nome' ou 'categoria'): ").strip().lower()

        if search_type == 'nome':
            search_term = View.get_input("Digite o nome do produto que deseja editar: ").strip()
            products = self.find_product_by_name(search_term)
        elif search_type == 'categoria':
            search_term = View.get_input("Digite a categoria do produto que deseja editar: ").strip()
            products = self.find_product_by_category(search_term)
        else:
            View.display_message("Opção inválida! Escolha 'nome' ou 'categoria'.")
            return

        if not products:
            View.display_message("Nenhum produto encontrado.")
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
            search_type = View.get_input("Deseja buscar por nome ou categoria? (Digite 'nome' ou 'categoria'): ").strip().lower()

            if search_type == 'nome':
                search_term = View.get_input("Digite o nome do produto que deseja remover: ").strip()
                products = self.find_product_by_name(search_term)
            elif search_type == 'categoria':
                search_term = View.get_input("Digite a categoria do produto que deseja remover: ").strip()
                products = self.find_product_by_category(search_term)
            else:
                View.display_message("Opção inválida! Escolha 'nome' ou 'categoria'.")
                return

            if not products:
                View.display_message("Nenhum produto encontrado.")
                return
            
            for product in products:
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
        
        search_type = View.get_input("Deseja buscar por nome ou categoria? (Digite 'nome' ou 'categoria'): ").strip().lower()

        if search_type == 'nome':
            search_term = View.get_input("Digite o nome do produto que deseja restocar: ").strip()
            products = self.find_product_by_name(search_term)
        elif search_type == 'categoria':
            search_term = View.get_input("Digite a categoria do produto que deseja restocar: ").strip()
            products = self.find_product_by_category(search_term)
        else:
            View.display_message("Opção inválida! Escolha 'nome' ou 'categoria'.")
            return

        if not products:
            View.display_message("Nenhum produto encontrado.")
            return
        
        for product in products:
            if product:
                quantity_input = View.get_input("Digite a quantidade que deseja restocar: ")
                try:
                    quantity_to_add = int(quantity_input)
                    if quantity_to_add <= 0:
                        View.display_message("A quantidade para restocar deve ser maior que zero.")
                        return
                    
                    product.quantity += quantity_to_add  # Adiciona a quantidade ao produto
                    product.update_status()  # Atualiza o status com a nova quantidade
                    
                    View.display_message(f"Produto restocado! Quantidade agora é {product.quantity}.")
                    
                    if product.status == ProductStatus.AVAILABLE:
                        View.display_message("Notificação enviada aos interessados!")

                except ValueError:
                    View.display_message("Quantidade inválida! Digite um número válido.")
            else:
                View.display_message("Produto não encontrado.")


    def deposit(self):
        View.display_message("\n--- Depósito ---")
        
        # Solicita o valor a ser depositado
        deposit_amount_input = View.get_input("Digite o valor a ser depositado: ")
        
        try:
            # Converte o valor para float e valida se é positivo
            deposit_amount = float(deposit_amount_input)
            if deposit_amount <= 0:
                View.display_message("O valor do depósito deve ser maior que zero.")
                return
            
            # Atualiza o saldo do usuário
            self.current_user.balance += deposit_amount
            
            View.display_message(f"Depósito realizado com sucesso! Seu novo saldo é R${self.current_user.balance:.2f}")
        
        except ValueError:
            View.display_message("Valor inválido! Por favor, insira um número válido.")

    def logout(self):
        View.display_message(f"Usuário {self.current_user.user_name} deslogado.")
        self.current_user = None

if __name__ == "__main__":
    controller = Controller()
    controller.display_banner()

