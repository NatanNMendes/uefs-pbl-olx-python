# Subject (Produto observável)
class ProductObservable:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, product):
        for observer in self._observers:
            observer.update(product)

# Observer (usuário)
class UserObserver:
    def __init__(self, user):
        self.user = user

    def notify(self, product):
        print(f"Olá {self.user_name}, o produto '{product.name}' agora está disponível!")

# No produto
class Product(ProductObservable):
    def __init__(self, name, description, price, category):
        super().__init__()
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.status = ProductStatus.AVAILABLE

    def update_status(self, status):
        self.status = status
        if status == ProductStatus.AVAILABLE:
            self.notify_observers()

    def notify_observers(self):
        for observer in self._observers:
            observer.notify(self)
