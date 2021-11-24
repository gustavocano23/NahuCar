from django.urls import path
from . import views

app_name = 'NahuCar'

urlpatterns = [

    #Url para Productos
    path('', views.products, name='products'),
    path('update-product/<int:uid>/', views.updateProduct, name='update-product'),
    path('delete-product/<int:uid>/', views.deleteProduct, name="delete-product"),

    #Url para Inventario
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/<int:uid>/', views.inventory, name='inventory_get'),
    path('inventory/<int:uid>/', views.inventory, name='inventory_update'),

    #Url para el Empleado
    path('employee/', views.employee, name='employee'),
    path('employee/update-employee/<int:uid>', views.updateEmployee, name = "update-employee"),
    path('employee/delete-employee/<int:uid>',views.deleteEmployee, name='delete-employee'),
    #Url para historial
    path('history/', views.history, name='history'),

    #Todavia no se va programar
    path('analysis/', views.analysis, name='analysis'),

]
