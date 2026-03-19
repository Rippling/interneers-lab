from product_csr.repositories.category_repository import CategoryRepository

class CategoryService :
    
    def __init__(self):
        self.repo = CategoryRepository()
        
    def get_all_categories(self):
        categories=self.repo.get_all()
        return [cate.to_dict() for cate in categories]
    
    def get_category(self,category_id):
        category = self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("category not found")
        return category.to_dict()
    
    def create_category(self , data):
        if not data.get("title"):
            raise ValueError("Title is required")
        
        category = self.repo.create(data)
        return category.to_dict()
            
    def update_category(self,category_id,data):
        category = self.repo.get_by_id(category_id)
        if not category:
            raise ValueError("category not found")
        
        updated = self.repo.update(category,data)
        return updated.to_dict() 
    
    def delete_category(self,category_id):
        category = self.repo.get_by_id(category_id)
        if not category :
            raise ValueError("category not found")
        
        self.repo.delete(category)
        return {"message":"catgeory deleted successfully"}
            