# Controller
class MarketplaceController:
    def __init__(self, product_controller, purchase_controller, user):
        self.product_controller = product_controller
        self.purchase_controller = purchase_controller
        self.user = user

    def show_products(self):
        products = self.product_controller.products
        ProductView.display_products(products=products)

    def view_cart(self):
        ProductView.display_cart(self.user)

    def purchase_products(self):
        self.purchase_controller.checkout(self.user)

    def view_wishlist(self):
        ProductView.display_wishlist(self.user)

# Exemplo de utilização
user = UserFactory.create_user(UserType.NATURAL_PERSON, "João", "joao123", "joao@example.com", "senha123", 12345678901, 30, "12345-678", 500.0)
product_controller = ProductController()
purchase_controller = PurchaseController()

app = MarketplaceController(product_controller, purchase_controller, user)

while True:
    choice = ProductView.user_login()
    if choice == 1:
        ProductView.display_products(product_controller.products)
    elif choice == 2:
        ProductView.display_cart(user)
    elif choice == 3:
        user.view_wishlist()
    elif choice == 4:
        purchase_controller.checkout(user)
    elif choice == 0:
        break
