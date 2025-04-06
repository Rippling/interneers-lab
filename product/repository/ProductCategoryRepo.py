from ..models.CategoryModel import ProductCategory
# from ..models.ProductModel import Product,ProductHistory

class ProductCategoryRepo:
    def create(self, category_data):                            #create new category
        return ProductCategory.objects.create(**category_data) 

    def find_all(self):                                         #fetch all categories
        return ProductCategory.objects.all()

    def find_by_id(self, category_id):                          #find category by id
        try:
            return ProductCategory.objects.get(id=category_id)
        except ProductCategory.DoesNotExist:
            return None
    
    def search_by_title(self, title):                     #find category by title
        if not title:
            return self.find_all()
        return ProductCategory.objects.filter(title__icontains=title)      #case insensitive search

    def update(self, category_id, category_data):                #update existing category by id
        try:
            category=ProductCategory.objects.get(id=category_id)
            for key,value in category_data.items():
                setattr(category, key, value)
            category.save()
            return category
        except ProductCategory.DoesNotExist:
            return None

    def delete(self, category_id):                              #delete category by id
        try:
            category=ProductCategory.objects.get(id=category_id)
            category.delete()
            return True
        except ProductCategory.DoesNotExist:
            return False
        
    # def add_prod_to_category(self, category_id, product_id):   #add prod. to ca specific category
    #     try:
    #         category=ProductCategory.objects.get(id=category_id)
    #         product=Product.objects.get(id=product_id)
            
    #         #check if product is already in this category
    #         if product.category == category:
    #             return False
            
    #         #update product's category
    #         product.category=category
    #         product.save()
    #         return True
    #     except (ProductCategory.DoesNotExist, Product.DoesNotExist):
    #         return False

    # def remove_prod_from_category(self, product_id):         #remove prod. from the assigned category
    #     try:
    #         product=Product.objects.get(id=product_id)
            
    #         if not product.category:
    #             return False
            
    #         #store the old version before making changes
    #         ProductHistory.create_version(product)
    #         product.category = None
    #         product.save()
    #         return True
    #     except Product.DoesNotExist:
    #         return False