class ProductError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class ProductNotFound(ProductError):
    def __init__(self, product_id=None, status_code=404):
        message = f"Product not found."
        if product_id:
            message += f" Product ID: {product_id}"
        else:
            message += f" Product ID: None"
        super().__init__(message, status_code)

class InvalidProductId(ProductError):
    def __init__(self, product_id=None):
        message = f"Invalid product ID."
        if product_id:
            message += f" Product ID: {product_id}"
        else:
            message += f" Product ID: None"
        super().__init__(message)

class InvalidData(Exception):
    def __init__(self, message=None):
       if message:
           super().__init__(message)
       else:
           super().__init__("Invalid data")

class CategoryError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
class InvalidCategoryId(CategoryError):
     def __init__(self, category_id=None):
        message = f"Invalid category ID."
        if category_id:
            message += f" Category ID: {category_id}"
        else:
            message += f" Category ID: None"
        super().__init__(message, status_code=400)

class CategoryNotFound(CategoryError):
    def __init__(self, category_id):
        message = f"Category not found ."
        if category_id:
            message += f" Category ID: {category_id}"
        else:
            message += f" Category ID: None"
        super().__init__(message, status_code=404)