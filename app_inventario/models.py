from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    dni        = models.CharField(max_length=13,unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name  = models.CharField(max_length=50, null=True, blank=True)
    address    = models.CharField(max_length=100, null=True, blank=True)
    telphone   = models.CharField(max_length=20, null=True, blank=True)
    user       = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Empleado: {self.first_name} {self.last_name}'

class Categories(models.Model):
    category_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name      = models.CharField(max_length=50, null=True, blank=True)
    product_existence = models.IntegerField(null=True,blank=True)
    product_price     = models.FloatField(null=True, blank=True)
    category          = models.ForeignKey(Categories,on_delete=models.CASCADE, null=True, blank=True)
    product_active    = models.CharField(max_length=1, default="1", null=True, blank=True)

    def __str__(self):
        return f'Producto: {self.product_name} | Existencia: {self.product_existence}'

class Inventories(models.Model):
    created_date    = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date    = models.DateTimeField(auto_now=True, null=True, blank=True)
    inventory_stock = models.IntegerField(null=True, blank=True)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

class InventoriesHistory(models.Model):
    TYPEACTION = {
        ('1', 'INSERTAR'),
        ('2', 'RETIRAR'),
    }
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quantity     =  models.IntegerField(null=True, blank=True)
    type_action  = models.CharField(max_length=1, choices=TYPEACTION, null=True, blank=True)
    inventory    = models.ForeignKey(Inventories,on_delete=models.CASCADE, null=True, blank=True)
