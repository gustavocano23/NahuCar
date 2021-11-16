from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required


#<== Pagina de productos ==>

#Mostrar e Insertar datos
@login_required
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
            inventory_stock = last_product.product_existence,
            product = id_last_product
        )
        insert_product_to_inventory.save()

        #Ultima accion del producto dependiendo del producto
        last_inventory_id =  Inventories.objects.all().filter(product=id_last_product).last()
        #Instancia del ultimo inventario ingresado dependiendo del producto
        id_inventory = Inventories.objects.get(pk=last_inventory_id.pk)
        #Insertar en Historial
        history = InventoriesHistory(
            quantity = product_quantity,
            inventory = id_inventory,
            type_action = 1,
        )
        history.save()
        return redirect(reverse("NahuCar:products"))
#Actualizar datos
@login_required
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
@login_required
def deleteProduct(request, uid):
    product_by_id = get_object_or_404(Product, pk=uid)
    product_by_id.product_active = "0"
    product_by_id.save()
    return redirect(reverse('NahuCar:products'))

#<== Pagina de Inventario ==>

#CRUD Inventario
@login_required
def inventory(request,uid=None):
    if (request.method == "GET" and uid is None):
        categories =Categories.objects.all()
        products =  Product.objects.all()
        inventory = Inventories.objects.all()
        history = InventoriesHistory.objects.all()
        ctx = {
            "count_categories": len(categories), 
            "count_products": len(products),
            "count_inventory":len(history), 
            "inventories": inventory,
        }
        return render(request, 'inventario/inventory.html', ctx)

    elif (request.method == "GET" and uid is not None):
        categories =Categories.objects.all()
        products =  Product.objects.all()
        inventory = Inventories.objects.all()
        history = InventoriesHistory.objects.all()
        inventory_by_id = get_object_or_404(Inventories, pk=uid)
        ctx = {
            "count_categories": len(categories), 
            "count_products": len(products),
            "count_inventory":len(history), 
            "inventories": inventory,
            "inventory_by_id":inventory_by_id
        }
        return render(request, 'inventario/inventory.html', ctx)
    
    elif (request.method == "POST" and uid is not None):

        inventory_by_id = get_object_or_404(Inventories, pk=uid)

        #Capturar valores del formulario
        action = int(request.POST.get('action'))
        quantity = int(request.POST.get('quantity'))
        
        if (action == 1):
            #Verificar si la cantidad es mayor que 0
            if (quantity > 0):
                #Actualizar el Inventario
                inventory_by_id.inventory_stock += quantity
                inventory_by_id.save()

                #Instancia del inventario
                id_inventory = Inventories.objects.get(pk=inventory_by_id.pk)

                #Insertar un nuevo registro en el historial
                history = InventoriesHistory(
                    quantity = quantity,
                    type_action = action,
                    inventory = id_inventory
                )
                history.save()
                return redirect(reverse('NahuCar:inventory'))
        elif (action == 2):
            if (inventory_by_id.inventory_stock < quantity):
                return
            else:
                #Actualizar el Inventario
                inventory_by_id.inventory_stock -= quantity
                inventory_by_id.save()

                #Instancia del inventario
                id_inventory = Inventories.objects.get(pk=inventory_by_id.pk)
                #Insertar un nuevo registro en el historial
                history = InventoriesHistory(
                    quantity = quantity,
                    type_action = action,
                    inventory = id_inventory
                )
                history.save()
                return redirect(reverse('NahuCar:inventory'))


#<== Pagina de Empleado ==> 
@login_required
def employee(request):
    if (request.method == "GET"):
        employees = Employee.objects.all()
        ctx = {"employees":employees}
        return render(request, 'inventario/employee.html', ctx)
    elif (request.method == "POST"):
        #Capturar lo valores
        dni = request.POST.get('employee-dni')
        employee_name = request.POST.get('employee-name')
        employee_lastName = request.POST.get('employee-last-name')
        telphone = request.POST.get('employee-telphone')
        address = request.POST.get('employee-address')

        #Almacenar los valore en la base de datos

        employees = Employee(
            dni = dni,
            first_name = employee_name,
            last_name = employee_lastName,
            address = address,
            telphone = telphone,
        )
        employees.save()
        return redirect(reverse('NahuCar:employee'))

@login_required
def updateEmployee(request, uid):
    if (request.method == "GET"):
        employee_by_id = get_object_or_404(Employee, pk=uid)
        employees = Employee.objects.all()

        ctx = {
            "employee_by_id": employee_by_id,
            "employees": employees,
        }
        
        return render(request,'inventario/employee.html', ctx)

    elif(request.method == "POST"):
        employee_by_id = get_object_or_404(Employee, pk=uid)
        #Capturamos los valores del formulario para actualizar
        dni = request.POST.get('employee-dni')
        employee_name = request.POST.get('employee-name')
        employee_lastName = request.POST.get('employee-last-name')
        telphone = request.POST.get('employee-telphone')
        address = request.POST.get('employee-address')

        #Actualizamos el empleado por el id
        employee_by_id.dni = dni
        employee_by_id.first_name = employee_name
        employee_by_id.last_name = employee_lastName
        employee_by_id.telphone =  telphone
        employee_by_id.address = address
        employee_by_id.save()
        return redirect(reverse('NahuCar:employee'))

@login_required
def deleteEmployee(request,uid):
    employee_by_id = Employee.objects.get(pk=uid)
    employee_by_id.delete()
    return redirect(reverse('NahuCar:employee'))

@login_required
def history(request):
    histories = InventoriesHistory.objects.all()[::-1]
    ctx = {"histories":histories}
    return render(request, 'inventario/history.html',ctx)


@login_required
def analysis(request): 
    return render(request, 'inventario/analysis.html')