from .repositories import ProductRepository
from .serializers import ProductSerializer
from django.http import Http404


class ProductService:

    @staticmethod
    def createProd(prod_details):

        ser = ProductSerializer(data = prod_details)
        
        if ser.is_valid():
            prod = ProductRepository.createProd(prod_details)
            return { "success": True , "data" : ProductSerializer(prod).data}
        
        return {"success" : False , "data" : ser.errors}
    

    @staticmethod
    def getAllProds():

        data = ProductRepository.getAllProd()
        return ProductSerializer(data, many= True).data
    

    @staticmethod
    def getProdById(prod_id):

        data = ProductRepository.getProdById(prod_id)

        if not data:
            raise Http404("Product not found")
        
        return data
    
  
    @staticmethod
    def updateProd(prod_id, prod_details):
        prod = ProductRepository.getProdById(prod_id)

        if not prod:
            return None  
        
        ser = ProductSerializer(prod, data=prod_details, partial=True)  
        
        if ser.is_valid():
            ser.save()  
            return prod  
        
        raise Exception(ser.errors)  

    

    @staticmethod
    def deleteProd(prod_id):

        TrueOrFalse = ProductRepository.deleteProd(prod_id)

        if TrueOrFalse:
            return {"success" : True , "message": "Product deleted successfully"}
        
        raise Http404("Product not found")