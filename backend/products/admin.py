from django.contrib import admin
# MongoEngine models can't be registered with Django admin
# Leaving this file for reference, but commenting out registrations

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'created_at', 'updated_at']
#     search_fields = ['name', 'description']
#     list_filter = ['created_at', 'updated_at']
#     prepopulated_fields = {'slug': ('name',)}
#     ordering = ['name']

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'sku', 'category', 'price', 'quantity', 'status', 'is_in_stock', 'is_low_stock']
#     list_filter = ['status', 'category', 'brand', 'featured']
#     search_fields = ['name', 'description', 'sku', 'brand']
#     prepopulated_fields = {'slug': ('name',)}
#     list_editable = ['status', 'quantity']
#     readonly_fields = ['uuid', 'created_at', 'updated_at']
#     fieldsets = [
#         ('Basic Information', {
#             'fields': ['sku', 'name', 'slug', 'description']
#         }),
#         ('Categorization', {
#             'fields': ['category', 'brand', 'tags']
#         }),
#         ('Pricing and Stock', {
#             'fields': ['price', 'discount_price', 'quantity', 'low_stock_threshold']
#         }),
#         ('Product Details', {
#             'fields': ['weight', 'dimensions']
#         }),
#         ('Status and Tracking', {
#             'fields': ['status', 'featured', 'rating']
#         }),
#         ('Metadata', {
#             'fields': ['uuid', 'created_at', 'updated_at'],
#             'classes': ['collapse']
#         })
#     ]
    
#     def is_in_stock(self, obj):
#         return obj.is_in_stock
#     is_in_stock.boolean = True
#     is_in_stock.short_description = 'In Stock'

#     def is_low_stock(self, obj):
#         return obj.is_low_stock
#     is_low_stock.boolean = True
#     is_low_stock.short_description = 'Low Stock'
