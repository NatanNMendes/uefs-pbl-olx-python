class AccountView:
    @staticmethod
    def criar_conta():
        print("\n=== Criar Conta ===")
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        return nome, email, senha

    @staticmethod
    def fazer_login():
        print("\n=== Fazer Login ===")
        email = input("Digite seu email: ")
        senha = input("Digite sua senha: ")
        return email, senha
