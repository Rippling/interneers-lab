from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=50)
    quantity_in_warehouse = models.IntegerField()

    def __str__(self):
        return self.name
