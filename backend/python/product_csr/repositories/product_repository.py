from product_csr.models import Product


class ProductRepository:

    def create(self, data):
        product = Product(**data)
        product.save()
        return product

    
    def get_all(self):
        return Product.objects()

    
    def get_by_id(self, product_id):
        return Product.objects(id=product_id).first()

    
    def update(self, product, data):
        product.name = data.get("name", product.name)
        product.brand = data.get("brand", product.brand)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)
        product.save()
        return product

    
    def delete(self, product):
        product.delete()

    
    def get_by_category(self, category):
        return Product.objects(category=category)