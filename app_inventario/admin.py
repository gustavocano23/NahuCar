from django.contrib import admin
from .models import *


admin.site.register(Employee)
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Inventories)
admin.site.register(InventoriesHistory)