from ..repositories.ProductRepository import ProductRepository
from ..repositories.Category import CategoryRepository
from ..serializers import ProductSerializer
from django.http import Http404
from bson import ObjectId

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
        return data


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
    
    @staticmethod
    def remove_category_from_product(product_id, category_id):
        product = ProductRepository.getProdById(product_id)
        category = CategoryRepository.getCategoryById(category_id)

        if not product:
            raise Http404("Product not found")
        if not category:
            raise Http404("Category not found")

        product_category_ids = [ObjectId(cat.id) for cat in product.category]

        for cat in product.category:
            print(cat.id, ObjectId(cat.id) )

        if ObjectId(category_id) not in product_category_ids:
            return {"message": "Category not assigned to product.", "status": 400}

        updated_categories = [cat for cat in product.category if ObjectId(cat.id) != ObjectId(category_id)]
        ProductRepository.update_product_categories(product, updated_categories)

        return {"message": "Category removed from product successfully.", "status": 200}
    
    @staticmethod
    def add_category_to_product(product_id, category_id):

        product = ProductRepository.getProdById(product_id)
        category = CategoryRepository.getCategoryById(category_id)

        if not product:
            raise Http404("Product not found.")
        if not category:
            raise Http404("Category not found.")

     
        product_category_ids = [ObjectId(cat.id) for cat in product.category]

        if category_id in product_category_ids:
            return {"message": "Category already assigned to product.", "status": 400}

        
        product.category.append(category)  
        product.save()

        return {"message": "Category added to product successfully.", "status": 200}

   