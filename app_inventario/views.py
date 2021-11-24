from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages


#<== Pagina de productos ==>

#Mostrar e Insertar datos
@login_required
def products(request):
    #<== Mostrar informacion en el template products ==>
    if (request.method == "GET"):
        categories = Categories.objects.all()
        
        # Obtiene el valor a buscar
        q = request.GET.get('q')

        # Motor de busqueda
        if q:
            if Product.objects.filter(product_name__startswith=q,product_active="1"):
                products = Product.objects.filter(product_name__startswith=q,product_active="1")
            elif Product.objects.filter(product_price__startswith=q,product_active="1"):
                products = Product.objects.filter(product_price__startswith=q,product_active="1")
            elif Product.objects.filter(product_existence__startswith=q,product_active="1"):
                products = Product.objects.filter(product_existence__startswith=q,product_active="1")
            elif Product.objects.filter(category__category_name__startswith=q,product_active="1"):
                products = Product.objects.filter(category__category_name__startswith=q,product_active="1")
            else:
                products = Product.objects.all().filter(product_active="1")
        else:
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
        messages.add_message(request, messages.INFO, f'Se ha registrado el producto correctamente')  
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

        messages.add_message(request, messages.INFO, f'Se ha actualizado el producto correctamente') 
        return redirect(reverse("NahuCar:products"))
#Desactivar datos de producto seleccionado por el usuario
@login_required
def deleteProduct(request, uid):
    product_by_id = get_object_or_404(Product, pk=uid)
    product_by_id.product_active = "0"
    product_by_id.save()
    messages.add_message(request, messages.INFO, f'Se ha borrado el producto correctamente') 
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
        
        # Obtiene el valor a buscar
        q = request.GET.get('q')
        
        # Motor de busqueda
        if q:
            if Inventories.objects.filter(id__startswith=q):
                inventory = Inventories.objects.filter(id__startswith=q).order_by('id')
            elif Inventories.objects.filter(updated_date__startswith=q):
                inventory = Inventories.objects.filter(updated_date__startswith=q).order_by('updated_date')
            elif Inventories.objects.filter(inventory_stock__startswith=q):
                inventory = Inventories.objects.filter(inventory_stock__startswith=q).order_by('inventory_stock')
            elif Product.objects.filter(product_name__startswith=q):
                inventory = Inventories.objects.filter(product__product_name__startswith=q)
            elif Product.objects.filter(product_price__startswith=q):
                inventory = Inventories.objects.filter(product__product_price__startswith=q)
            elif Categories.objects.filter(category_name__startswith=q):
                category_resultado = Categories.objects.filter(category_name__startswith=q)
                inventario = ""
                for x in category_resultado:
                    if Product.objects.filter(category=x):
                        inventory = Inventories.objects.filter(product__category=x)
                    elif inventario=="":
                        inventory = Inventories.objects.all()
            else:
                inventory = Inventories.objects.all()
        else:
            inventory = Inventories.objects.all()

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
        history = InventoriesHistory.objects.all()
        inventory_by_id = get_object_or_404(Inventories, pk=uid)
        inventory = Inventories.objects.all()

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

                messages.add_message(request, messages.INFO, f'Se ha actualizado el inventario') 
                return redirect(reverse('NahuCar:inventory'))
            else:
                messages.add_message(request, messages.INFO, f'La cantidad debe de ser mayor que 0')
                return redirect(reverse('NahuCar:inventory')) 
        elif (action == 2):
            if (inventory_by_id.inventory_stock < quantity):
                messages.add_message(request, messages.INFO, f'La cantidad no debe ser mayor a la cantidad inventariada')
                return redirect(reverse('NahuCar:inventory'))
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
                messages.add_message(request, messages.INFO, f'Se actualizo el inventario correctamente')
                return redirect(reverse('NahuCar:inventory'))


#<== Pagina de Empleado ==> 
@login_required
def employee(request):
    if (request.method == "GET"):

        # Obtiene el valor a buscar
        q = request.GET.get('q')

        # Motor de busqueda
        if q:
            if Employee.objects.filter(dni__startswith=q):
                employees = Employee.objects.filter(dni__startswith=q)
            elif Employee.objects.filter(first_name__startswith=q):
                employees = Employee.objects.filter(first_name__startswith=q)
            elif Employee.objects.filter(last_name__startswith=q):
                employees = Employee.objects.filter(last_name__startswith=q)
            elif Employee.objects.filter(address__startswith=q):
                employees = Employee.objects.filter(address__startswith=q)
            elif Employee.objects.filter(telphone__startswith=q):
                employees = Employee.objects.filter(telphone__startswith=q)
            else:
                employees = Employee.objects.all()
        else:
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

        #Almacenar los valores en la base de datos

        employees = Employee(
            dni = dni,
            first_name = employee_name,
            last_name = employee_lastName,
            address = address,
            telphone = telphone,
        )
        employees.save()

        password = make_password("123ABcd.")

        #traer el ultimo empleado a registrado
        last_employee = Employee.objects.all().last()
        username = f'{employee_name[0]}{employee_lastName}'
        user = User(
            username = username,
            password = password,
        )
        user.save()

        #traer el ultimo usuario ingresado
        last_user = User.objects.all().last()

        #Instancia del ultimo usuario
        last_user_id = User.objects.get(pk=last_user.pk)

        #Asignar el usuario y la contraseña
        last_employee.user = last_user_id
        last_employee.save()     
        messages.add_message(request, messages.INFO, f'Se ha guardado con exito, El usuario es: {username}')   
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
        messages.add_message(request, messages.INFO, f'Se ha actualizado el empleado correctamente')
        return redirect(reverse('NahuCar:employee'))

@login_required
def deleteEmployee(request,uid):
    employee_by_id = Employee.objects.get(pk=uid)
    employee_by_id.delete()
    messages.add_message(request, messages.INFO, f'Se ha borrado el empleado correctamente')
    return redirect(reverse('NahuCar:employee'))

@login_required
def history(request):
    histories = InventoriesHistory.objects.all()[::-1]

    # Obtiene el valor a buscar
    q = request.GET.get('q')

    # Motor de busqueda
    if q:
        if InventoriesHistory.objects.filter(id__startswith=q):
            histories = InventoriesHistory.objects.filter(id__startswith=q)[::-1]
        elif InventoriesHistory.objects.filter(inventory__product__product_name__startswith=q):
            histories = InventoriesHistory.objects.filter(inventory__product__product_price__startswith=q)[::-1]
        elif InventoriesHistory.objects.filter(inventory__product__product_price__startswith=q):
            histories = InventoriesHistory.objects.filter(inventory__product__product_price__startswith=q)[::-1]
        elif InventoriesHistory.objects.filter(quantity__startswith=q):
            histories = InventoriesHistory.objects.filter(quantity__startswith=q)[::-1]
        elif InventoriesHistory.objects.filter(inventory__product__category__category_name__startswith=q):
            histories = InventoriesHistory.objects.filter(inventory__product__category__category_name__startswith=q)[::-1]
        else:
            histories = InventoriesHistory.objects.all()[::-1]
    else:
        histories = InventoriesHistory.objects.all()[::-1]

    ctx = {"histories":histories}
    return render(request, 'inventario/history.html',ctx)


@login_required
def analysis(request): 
    return render(request, 'inventario/analysis.html')