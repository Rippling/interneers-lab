# bridge between views and repository
from .repository import product_repository


class ProductService:
    def create(self, data):
        return product_repository.create(data)

    def get(self, id):
        return product_repository.get(id)

    def list_all(self):
        return product_repository.list_all()

    def update(self, id, data):
        return product_repository.update(id, data)

    def delete(self, id):
        return product_repository.delete(id)


product_service = ProductService()
