from product.repository.product import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
    
    def create_product(self, data):
        if 'name' not in data or 'price' not in data:
            raise ValueError("Product 'name' and 'price' are required.")
        return self.repository.create_product(data)

    def get_product(self, product_id):
        product = self.repository.get_product(product_id)
        if not product:
            raise ValueError("Product not found.")
        return product
    
    def get_all_products(self):
        return self.repository.get_all_products()
    
    def update_product(self, product_id, data):
        product = self.repository.update_product(product_id, data)
        if not product:
            raise ValueError("Product not found for update.")
        return product

    def delete_product(self, product_id):
        product = self.repository.delete_product(product_id)
        if not product:
            raise ValueError("Product not found for deletion.")
        return product
    