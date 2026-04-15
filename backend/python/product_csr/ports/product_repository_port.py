from abc import ABC, abstractmethod


class ProductRepositoryPort(ABC):
    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def get_all(self, owner_id=None):
        pass

    @abstractmethod
    def filter_products(self, filters, owner_id=None):
        pass

    @abstractmethod
    def get_by_id(self, product_id):
        pass

    @abstractmethod
    def update(self, product, data):
        pass

    @abstractmethod
    def delete(self, product):
        pass

    @abstractmethod
    def get_by_category(self, category, owner_id=None):
        pass
