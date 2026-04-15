from abc import ABC, abstractmethod


class CategoryRepositoryPort(ABC):
    @abstractmethod
    def get_all(self, owner_id=None):
        pass

    @abstractmethod
    def get_by_id(self, category_id, owner_id=None):
        pass

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def update(self, category, data):
        pass

    @abstractmethod
    def delete(self, category):
        pass

    @abstractmethod
    def get_by_title(self, title, owner_id=None):
        pass
