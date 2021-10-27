from django.shortcuts import render


def index(request):
    return render(request, 'inventario/index.html')

def page1(request):
    return render(request,'inventario/page1.html')