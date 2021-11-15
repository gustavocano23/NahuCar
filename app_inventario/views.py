from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import *


#<== Pagina de productos ==>

#Mostrar e Insertar datos
def products(request):
    #<== Mostrar informacion en el template products ==>
    if (request.method == "GET"):
        categories = Categories.objects.all()
        products = Product.objects.all().filter(product_active="1")
        ctx = {
            "categories": categories,
            "products":products,
        }
        return render(request,'inventario/products.html', ctx)
    elif (request.method == "POST"):
        #Capturar valores del formulario
        product_name = request.POST.get("product-name")
        product_price = float(request.POST.get("price"))
        product_quantity = int(request.POST.get("quantity"))
        product_category = int(request.POST.get("category"))

        #capturar la instancia de la categoria del producto
        id_category = Categories.objects.get(pk=product_category)
        
        #Guardar los valores en la tabla Products
        product = Product(
            product_name = product_name,
            product_existence  = product_quantity, 
            product_price = product_price,
            category = id_category,
        )
        product.save()

        #Insertar en el inventario el nuevo producto
        last_product = Product.objects.all().last()
        #Instancia del ultimo producto ingresado
        id_last_product = Product.objects.get(pk=last_product.id)
        insert_product_to_inventory = Inventories(
            type_action = '1',
            inventory_stock = last_product.product_existence,
            product = id_last_product
        )
        insert_product_to_inventory.save()

        return redirect(reverse("NahuCar:products"))
#Actualizar datos
def updateProduct(request, uid):
    product_by_id = get_object_or_404(Product, pk=uid)

    if (request.method == "GET"):
        categories = Categories.objects.all()
        products = Product.objects.all().filter(product_active="1")
        ctx = {
            "product_by_id": product_by_id,
            "categories": categories,
            "products":products,
        }
        return render(request, 'inventario/products.html',ctx)

    elif (request.method == "POST"):
        
        #Capturar valores del formulario
        product_name = request.POST.get("product-name")
        product_price = float(request.POST.get("price"))
        product_quantity = int(request.POST.get("quantity"))
        product_category = int(request.POST.get("category"))

        #capturar la instancia de la categoria del producto
        id_category = Categories.objects.get(pk=product_category)

        #Actualizar informacion
        product_by_id.product_name = product_name
        product_by_id.product_price = product_price
        product_by_id.product_existence = product_quantity
        product_by_id.category = id_category
        product_by_id.save()


        return redirect(reverse("NahuCar:products"))
#Desactivar datos de producto seleccionado por el usuario
def deleteProduct(request, uid):
    product_by_id = get_object_or_404(Product, pk=uid)
    product_by_id.product_active = "0"
    product_by_id.save()
    return redirect(reverse('NahuCar:products'))
    

def inventory(request,uid=None):
    if (request.method == "GET" and uid is None):
        categories =Categories.objects.all()
        products =  Product.objects.all()
        inventory = Inventories.objects.all()
        ctx = {
            "count_categories": len(categories), 
            "count_products": len(products),
            "count_inventory":len(inventory), 
            "inventories": inventory,
        }
        return render(request, 'inventario/inventory.html', ctx)
    elif (request.method == "GET" and uid is not None):
        inventory_by_id = get_object_or_404(Inventories, pk=uid)
        return render(request, 'inventario/inventory.html', {"inventory_by_id":inventory_by_id})
        
    

def history(request):
    return render(request, 'inventario/history.html')

def employee(request):
    return render(request, 'inventario/employee.html')

def analysis(request): 
    return render(request, 'inventario/analysis.html')