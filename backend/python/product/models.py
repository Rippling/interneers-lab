from django.db import models

# Create your models here.
# product model (no db becoz of in memory only)

class Product :
    def __init__(self,id,name,desc,category,price,brand,quantity):
        self.id = id 
        self.name = name 
        self.desc = desc
        self.category = category
        self.price = price
        self.brand = brand 
        self.quantity = quantity
