# admin.py
from django_mongoengine.mongo_admin import site
from .models import Products
from django_mongoengine.mongo_admin import DocumentAdmin

class ProductAdmin(DocumentAdmin):
    form_columns = ['int_id', 'name', 'description']

site.register(Products, ProductAdmin)

