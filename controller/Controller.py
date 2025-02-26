class Controller:
    def __init__(self):
        self.produtos = []  # Lista para armazenar os produtos
        self.conta_criada = False
        self.usuario_logado = None

    def executar(self):
        while True:
            # Exibir logo
            MarketplaceView.exibir_logo()

            # Menu principal
            opcao = MarketplaceView.menu_principal()
            if opcao == 'criar_conta':
                nome, email, senha = AccountView.criar_conta()
                self.conta_criada = True
                MarketplaceView.exibir_mensagem_sucesso("Conta criada")
            elif opcao == 'fazer_login':
                email, senha = AccountView.fazer_login()
                if self.conta_criada:
                    self.usuario_logado = email  # Simulando login
                    MarketplaceView.exibir_mensagem_sucesso("Login realizado")
                else:
                    MarketplaceView.exibir_mensagem_erro("Conta não encontrada")

            # Menu opções após login
            if self.usuario_logado:
                while True:
                    opcao = MarketplaceView.menu_opcoes()

                    if opcao == '1':
                        ProductView.exibir_produtos(self.produtos)
                    elif opcao == '2':
                        nome, descricao, preco, categoria = ProductView.cadastrar_produto()
                        novo_produto = Product(nome, descricao, preco, categoria)
                        self.produtos.append(novo_produto)
                        MarketplaceView.exibir_mensagem_sucesso("Produto cadastrado")
                    elif opcao == '3':
                        produto_id = ProductView.remover_produto(self.produtos)
                        produto = next((p for p in self.produtos if p.id == produto_id), None)
                        if produto:
                            self.produtos.remove(produto)
                            MarketplaceView.exibir_mensagem_sucesso("Produto removido")
                    elif opcao == '5':
                        print("Saindo...")
                        break
