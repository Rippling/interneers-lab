from .repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()       # initialize ProductRepository instance

    # service methods which call corr. ProductRepository methods to perform diff. tasks

    def create_product(self,prod_data):
        return self.repository.create(prod_data)
    
    def get_all_products(self):
        return self.repository.get_all()
    
    def get_product_by_id(self,prod_id):
        return self.repository.get_by_id(prod_id)
    
    def update_product(self,prod_id, prod_data):
        return self.repository.update(prod_id, prod_data)
    
    def delete_product(self,prod_id):
        return self.repository.delete(prod_id)