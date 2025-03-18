from .repository import ProductRepository
class ProductService:
    @staticmethod
    def list_products():
        return ProductRepository.get_all()

    @staticmethod
    def get_product(product_id):
        print("getting",product_id)
        return ProductRepository.get_by_id(product_id)

    @staticmethod
    def create_product(data):
        return ProductRepository.create(data)

    @staticmethod
    def update_product(product_id, data):
        product = ProductRepository.get_by_id(product_id)
        if product:
            return ProductRepository.update(product, data)
        return None

    @staticmethod
    def delete_product(product_id):
        product = ProductRepository.get_by_id(product_id)
        if product:
            ProductRepository.delete(product)
            return True
        return False