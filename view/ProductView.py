class ProductView:
    @staticmethod
    def display_products(products):
        for product in products:
            print(f"ID: {product.id} - Nome: {product.name} - Categoria: {product.category} - Preço: R${product.price:.2f} - Status: {product.status}")

    @staticmethod
    def display_cart(user):
        print("Carrinho:")
        for product in user.cart:
            print(f"{product.name} - R${product.price:.2f}")

    @staticmethod
    def display_purchased_products(user):
        print("Produtos comprados:")
        for product in user.purchased_products:
            print(f"{product.name} - R${product.price:.2f}")

    @staticmethod
    def display_wishlist(user):
        print("Lista de desejos:")
        for product in user.wishlist:
            print(f"{product.name}")
