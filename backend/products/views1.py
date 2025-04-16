from django.shortcuts import render
import os
from django.conf import settings

def show_product_page(request):
    return render(request, 'user/product/product_list.html')

def product_detail_view(request, id):
    return render(request, 'user/product/prod_detail.html', {'product_id': id})

def show_categories_page(request):
    return render(request, 'user/category/category_list.html')

def category_detail_view(request, title):                                                        #Shows products belonging to a specific category.
    return render(request, 'user/category/category_detail.html', {'category_title': title})
