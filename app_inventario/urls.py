from django.urls import path
from . import views

app_name = 'NahuCar'

urlpatterns = [
    path('', views.products, name='products'),
    path('inventory/', views.inventory, name='inventory'),
    path('history/', views.history, name='history'),
    path('employee/', views.employee, name='employee'),
    path('analysis/', views.analysis, name='analysis'),

]
