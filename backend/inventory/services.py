from .repositories import ProductRepository

class ProductService:
    @staticmethod
    def get_all_products():
        products = ProductRepository.get_all_products()
        return [{
            "id" : str(p.id), "name":p.name, "price":p.price, "quantity":p.quantity, "created_at":p.created_at, "updated_at":p.updated_at
        } for p in products]

    @staticmethod
    def get_product_by_id(id):
        product = ProductRepository.get_product_by_id(id)
        if product: 
            return {"id" : str(product.id), "name":product.name, "price":product.price, "quantity":product.quantity, "created_at":product.created_at, "updated_at":product.updated_at}
        return None

    @staticmethod
    def create_new_product(product_data):
        if ProductRepository.get_all_products().filter(name=product_data['name']).count() > 0:
            return {"error" : "Product already exists. Kindly update the product instead of trying to create new product."}
        
        product = ProductRepository.create_product(product_data)
        return {"id":str(product.id), "name":product.name, "price":product.price, "quantity":product.quantity, "created_at":product.created_at, "updated_at":product.updated_at}
    
    def update_product(id, product_data):
        product = ProductRepository.get_product_by_id(id)
        if not product:
            return {"error" : "Product not found. Kindly create new one."}
        product = ProductRepository.update_product(product, product_data)
        return {"id":str(product.id), "name":product.name, "price":product.price, "quantity":product.quantity, "created_at":product.created_at, "updated_at":product.updated_at}
    
    def delete_product(id):
        product = ProductRepository.get_product_by_id(id)
        if not product: 
            return {"error": "Product not found."}
        ProductRepository.delete_product(product)
        return {"success": "Product deleted."}
