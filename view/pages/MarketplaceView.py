class MarketplaceView:
    @staticmethod
    def exibir_logo():
        logo = """                                @@@@@@@@                                       
                                @@@@@@@@@                                       ...
                                """
        print(logo)
        time.sleep(3)
        clear_screen()

    @staticmethod
    def menu_principal():
        print("OLX -> Tela Inicial\n")
        print("Olá!!! Seja Bem-Vindo\n")
        print("1 - Criar Conta")
        print("2 - Fazer Login")
        
        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            return 'criar_conta'
        elif opcao == '2':
            return 'fazer_login'
        else:
            print("Opção inválida!!!")
            time.sleep(2)
            clear_screen()
            return MarketplaceView.menu_principal()

    @staticmethod
    def menu_opcoes():
        print("OLX -> Tela Menu\n")
        print("1 - Comprar Produto")
        print("2 - Cadastrar Produto")
        print("3 - Editar Produto")
        print("4 - Remover Produto")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")
        return opcao

    @staticmethod
    def exibir_mensagem_sucesso(mensagem):
        print(f"{mensagem} com sucesso!")
        time.sleep(2)

    @staticmethod
    def exibir_mensagem_erro(mensagem):
        print(f"Erro: {mensagem}")
        time.sleep(2)
        
    @staticmethod
    def exibir_produtos(produtos):
        if not produtos:
            print("Nenhum produto disponível.\n")
            return

        print("\nProdutos disponíveis:")
        for produto in produtos:
            print(f"ID: {produto.id} - Nome: {produto.name} - Preço: R$ {produto.price} - Status: {produto.status.value}")
        print("\n")
        
    @staticmethod
    def exibir_produto(produto):
        if produto:
            print(f"Produto {produto.name}:")
            print(f"Descrição: {produto.description}")
            print(f"Preço: R$ {produto.price}")
            print(f"Categoria: {produto.category.value}")
            print(f"Status: {produto.status.value}")
        else:
            print("Produto não encontrado.\n")
