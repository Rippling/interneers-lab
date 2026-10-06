# store.py : temporary in-memory database

from .models import Product


class ProductStore:
    def __init__(self):
        self.products = {}
        self.next_id = 1

    # creating new data

    def create(self, data):
        # it is python object not JSON
        product = Product(
            id=self.next_id,
            name=data["name"],
            description=data["description"],
            category=data["category"],
            price=data["price"],
            brand=data.get("brand", ""),
            quantity=data["quantity"],
        )
        self.products[self.next_id] = product
        self.next_id += 1
        return product

    # getting existing data

    def get(self, product_id):
        return self.products.get(product_id)

    # listing all data

    def list_all(self):
        return list(self.products.values())

    # updating data

    def update(self, product_id, data):
        product = self.products.get(product_id)
        if not product:
            return None
        product.name = data["name"]
        product.description = data["description"]
        product.category = data["category"]
        product.price = data["price"]
        product.brand = data.get("brand", "")
        product.quantity = data["quantity"]
        return product

    # deleting data

    def delete(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False


product_store = ProductStore()
