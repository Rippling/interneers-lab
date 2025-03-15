from .models import Product

class ProductRepository:
    def create(self, prod_data):             # creates new product
        product=Product(**prod_data)
        product.save()
        return product
    
    def get_all(self):                                  # fetches all products
        return Product.objects.all()       
    
    def get_by_id(self, prod_id):                          # fetches product on the basis of id
        try:
            return Product.objects.get(id=prod_id)       
        except Product.DoesNotExist:
            return None
    
    def update(self, prod_id, prod_data):           # updates product on the basis of id
        try:
            product = Product.objects.get(id=prod_id)
            for key, value in prod_data.items():
                setattr(product, key, value)
            product.save()                          # save updated product
            return product
        except Product.DoesNotExist:
            return None
    
    def delete(self, prod_id):                      # deletes product on the basis of id
        try:
            product = Product.objects.get(id=prod_id)
            product.delete()
            return True
        except Product.DoesNotExist:
            return False