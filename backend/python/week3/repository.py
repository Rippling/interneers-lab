# replacement for store in week 2
# here i replaced in memory store with repository layer having same CRUD interface but with mongoDB using mongoengine
from datetime import datetime
from .models import Product


class ProductRepository:
    # create new product
    def create(self, data):
        product = Product(
            name=data["name"],
            description=data["description"],
            category=data["category"],
            price=data["price"],
            brand=data.get("brand", ""),
            quantity=data["quantity"],
            updated_at=datetime.utcnow(),
        )
        # tells mongoengine to persist this document in mongodb
        # so mongoengine looks at the model, sees meta = {"" : ""} connects through default mongodb connection and inserts an new doc into the product collection
        product.save()
        return product

    # get specific product by id
    def get(self, id):
        return Product.objects(id=id).first()

    # list all products
    def list_all(self):
        return Product.objects.all()

    # update product
    def update(self, id, data):
        product = self.get(id)
        if not product:
            return None

        product.name = data["name"]
        product.description = data["description"]
        product.category = data["category"]
        product.price = data["price"]
        product.brand = data.get("brand", "")
        product.quantity = data["quantity"]
        product.updated_at = datetime.utcnow()
        product.save()
        return product

    # delete product
    def delete(self, id):
        product = self.get(id)
        if not product:
            return False
        product.delete()
        return True


product_repository = ProductRepository()
