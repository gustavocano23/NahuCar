"""NahuCar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls import include
from django.conf import settings
from app_inventario import views
from app_seguridad import views

urlpatterns = [
    # Urls para el admin de django
    path('admin/', admin.site.urls),

    # Urls para el inicio de sesion
    path('', views.page_login, name='page_login'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'), 

    # Urls para la app de Inventario NahuCar
    path('NahuCar/', include('app_inventario.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
