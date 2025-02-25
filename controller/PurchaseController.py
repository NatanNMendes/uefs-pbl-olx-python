class PurchaseController:
    def checkout(self, user):
        total = sum(prod.price for prod in user.cart)
        if user.wallet >= total:
            user.wallet -= total
            user.purchased_products.extend(user.cart)
            user.cart.clear()
            return True
        return False

    def add_to_cart(self, user, product):
        user.cart.append(product)

    def remove_from_cart(self, user, product):
        if product in user.cart:
            user.cart.remove(product)