class MarketplaceView:
    @staticmethod
    def main_menu():
        print("\n=== Marketplace ===")
        print("[1] Visualizar Produtos")
        print("[2] Meu Carrinho")
        print("[3] Lista de Desejos")
        print("[4] Comprar Produtos")
        print("[0] Sair")
        return int(input("Selecione uma opção: "))

    @staticmethod
    def user_login():
        username = input("Digite seu nome de usuário: ")
        password = input("Digite sua senha: ")
        return username, password