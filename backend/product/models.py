from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)
    quantity = models.IntegerField()
    manufacture_date = models.DateField()
    expiry_date = models.DateField()  # for food, medicine, and items with a shelf life
    weight = models.FloatField() 

    def __str__(self):
        return self.name
