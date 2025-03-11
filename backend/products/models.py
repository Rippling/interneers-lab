from django.db import models

class Product(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank=True , null = True)
    category = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10 , decimal_places =2)
    brand = models.CharField(max_length =100 , blank=True, null = True)
    quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=255 , blank=True , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name
    

