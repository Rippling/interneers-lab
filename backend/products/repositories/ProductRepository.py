from ..models.ProductModel import Product
from bson import ObjectId

class ProductRepository:
    
    @staticmethod
    def createProd(prod_details):
        prod_details["price"] = float(prod_details["price"])
        prod = Product(**prod_details)
        prod.save()
        return prod 
    

    @staticmethod
    def getAllProd():
        return list(Product.objects.all())
    

    @staticmethod
    def getProdById(prod_id):
        try:
            return Product.objects.get(id = ObjectId(prod_id))
        
        except Product.DoesNotExist:
            return None


    @staticmethod
    def updateProd(prod_id , prod_details):

        prod = ProductRepository.getProdById(prod_id)

        if prod:
            for key,value in prod_details.items(): 
                setattr(prod,key,value)
            prod.save()
            return prod
        
        return None
    

    @staticmethod
    def deleteProd(prod_id):

        prod = ProductRepository.getProdById(prod_id)

        if prod:
            prod.delete()
            return True
        
        return None
     

    @staticmethod
    def update_product_categories(product, updated_categories):
        product.category = updated_categories
        product.save()
        
    