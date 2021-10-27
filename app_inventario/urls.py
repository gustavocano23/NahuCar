from django.urls import path
from . import views

app_name = 'NahuCar'

urlpatterns = [
    path('', views.page1, name='page1')
]
