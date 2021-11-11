from django.shortcuts import render


def index(request):
    return render(request, 'inventario/index.html')

def products(request):
    return render(request,'inventario/products.html')

def inventory(request):
    return render(request, 'inventario/inventory.html')

def history(request):
    return render(request, 'inventario/history.html')

def employee(request):
    return render(request, 'inventario/employee.html')

def analysis(request): 
    return render(request, 'inventario/analysis.html')