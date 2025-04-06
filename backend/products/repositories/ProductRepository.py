from ..models.ProductModel import Product
from bson import ObjectId
from bson.errors import InvalidId

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
            obj_id = ObjectId(prod_id)
            return Product.objects.get(id=obj_id)
        
        except InvalidId:
            raise ValueError("Invalid ID format. Must be a 12-byte input or 24-character hex string.")

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
        print(f"Looking for product with ID: {prod_id}")
        prod = ProductRepository.getProdById(prod_id)
        print(f"Product fetched: {prod}")

        if prod:
            prod.delete()
            return True
        
        return None
        
     

    @staticmethod
    def update_product_categories(product, updated_categories):
        product.category = updated_categories
        product.save()
        
    