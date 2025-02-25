class ProductController:
    def __init__(self):
        self.products = []

    def add_product(self, user, product):
        user.my_products.append(product)
        self.products.append(product)

    def remove_product(self, user, product):
        if product in user.my_products:
            user.my_products.remove(product)
            self.products.remove(product)

    def edit_product(self, product, name=None, category=None, price=None):
        if name:
            product.name = name
        if category:
            product.category = category
        if price:
            product.price = price

    def search_products(self, name=None, category=None):
        result = self.products
        if name:
            result = [prod for prod in result if name.lower() in prod.name.lower()]
        if category:
            result = [prod for prod in result if prod.category == category]
        return result
