from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=60)
    price = models.IntegerField()
    brand = models.CharField(max_length=60)
    quantity = models.IntegerField()


    def __str__(self):
        return self.name