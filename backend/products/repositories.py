from .models import Product

class ProductRepository:
    
    @staticmethod
    def createProd(prod_details):
        prod = Product(**prod_details)
        prod.save()
        return prod 
    

    @staticmethod
    def getAllProd():
        return Product.objects.all()
    

    @staticmethod
    def getProdById(prod_id):
        try:
            return Product.objects.get(id = prod_id)
        
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
     
        
    