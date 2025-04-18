from mongoengine import Document, StringField, signals

class ProductCategory(Document):
    title = StringField(required=True, max_length=100)
    description = StringField()

    meta = {'collection': 'product_categories'}

    def __str__(self):
        return self.title

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        """
        Signal handler that is called after a ProductCategory is deleted.
        It finds all Product documents whose 'category' field references the deleted category
        and sets that field to None.
        """
        # Delay the import to avoid circular dependency
        from product.models.product import Product
        # Update all products referencing the deleted category.
        Product.objects(category=document).update(set__category=None)

# Connect the post_delete signal to the ProductCategory model.
signals.post_delete.connect(ProductCategory.post_delete, sender=ProductCategory)