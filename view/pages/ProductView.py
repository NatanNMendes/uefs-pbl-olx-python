class ProductView:
    @staticmethod
    def cadastrar_produto():
        print("\n=== Cadastrar Produto ===")
        nome = input("Digite o nome do produto: ")
        descricao = input("Digite a descrição do produto: ")
        preco = float(input("Digite o preço do produto (R$): "))

        print("\nEscolha a categoria:")
        for idx, categoria in enumerate(ProductCategory, start=1):
            print(f"{idx} - {categoria.value}")

        categoria_opcao = int(input("\nDigite o número da categoria: "))
        categorias_lista = list(ProductCategory)
        categoria_escolhida = categorias_lista[categoria_opcao - 1]

        return nome, descricao, preco, categoria_escolhida

    @staticmethod
    def editar_produto(produto):
        if produto:
            print(f"\nO que você gostaria de editar no produto {produto.name}?")
            print("1 - Nome")
            print("2 - Descrição")
            print("3 - Preço")
            print("4 - Categoria")
            opcao_editar = int(input("\nEscolha uma opção: "))

            if opcao_editar == 1:
                novo_nome = input(f"Digite o novo nome (atual: {produto.name}): ")
                return 'nome', novo_nome
            elif opcao_editar == 2:
                nova_descricao = input(f"Digite a nova descrição (atual: {produto.description}): ")
                return 'descricao', nova_descricao
            elif opcao_editar == 3:
                novo_preco = float(input(f"Digite o novo preço (atual: R$ {produto.price}): "))
                return 'preco', novo_preco
            elif opcao_editar == 4:
                print("\nEscolha a nova categoria:")
                for idx, categoria in enumerate(ProductCategory, start=1):
                    print(f"{idx} - {categoria.value}")
                categoria_opcao = int(input("\nDigite o número da nova categoria: "))
                categorias_lista = list(ProductCategory)
                nova_categoria = categorias_lista[categoria_opcao - 1]
                return 'categoria', nova_categoria
        else:
            return None, None

    @staticmethod
    def remover_produto(produtos):
        if not produtos:
            print("Nenhum produto cadastrado.\n")
            return None

        print("\nProdutos cadastrados:")
        for produto in produtos:
            print(f"ID: {produto.id} - Nome: {produto.name}")

        produto_id = int(input("\nDigite o ID do produto que deseja remover: "))
        return produto_id
