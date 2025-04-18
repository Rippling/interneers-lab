from product.models.product import Product  

class ProductRepository:
    def create_product(self, data):
        product = Product(**data)
        product.save()
        return product
    
    def get_product(self, product_id):
        product = Product.objects(id=product_id).first()
        return product
    
    def get_all_products(self):
        products = Product.objects.all()
        return products
    
    def update_product(self, product_id, data):
        product = Product.objects(id=product_id).first()
        if product:
            product.update(**data)
            # it will return old data

            #if i want new data, i will have to re-fetch it like below
            # product = Product.objects(id=product_id).first()
        return product

    def delete_product(self, product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
        return product
    
