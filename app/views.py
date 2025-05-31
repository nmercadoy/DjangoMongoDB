from django.shortcuts import render, redirect
from .models_mongo import Producto
from mongoengine.errors import ValidationError
from bson import ObjectId
import re

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'app/lista.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        stock_raw = request.POST.get('stock', '').strip()

        errores = {}

        if not re.fullmatch(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+', nombre):
            errores['Nombre'] = 'Solo se permiten letras y espacios.'

        if len(descripcion) < 5 or len(descripcion) > 10:
            errores['Descripción'] = 'Debe tener entre 5 y 10 caracteres.'

        if '-' in stock_raw:
            errores['Stock'] = 'No se permite el uso del signo "-".'
        else:
            try:
                stock = int(stock_raw)
                if stock < 1:
                    errores['Stock'] = 'Solo se permiten números positivos mayores a 0.'
            except ValueError:
                errores['Stock'] = 'Debe ser un número válido.'

        if not errores:
            producto = Producto(
                nombre=nombre,
                descripcion=descripcion,
                stock=stock
            )
            try:
                producto.save()
                return redirect('lista_productos')
            except ValidationError as e:
                errores = {k.capitalize(): str(v[0]) for k, v in e.to_dict().items()}

        return render(request, 'app/crear.html', {
            'errores': errores,
            'nombre': nombre,
            'descripcion': descripcion,
            'stock': stock_raw,
            'producto': None
        })

    return render(request, 'app/crear.html', {
        'errores': {},
        'nombre': '',
        'descripcion': '',
        'stock': '',
        'producto': None
    })

def editar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=ObjectId(producto_id))
    except Producto.DoesNotExist:
        return redirect('lista_productos')

    errores = {}

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        stock_raw = request.POST.get('stock', '').strip()

        if not re.fullmatch(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+', nombre):
            errores['Nombre'] = 'Solo se permiten letras y espacios.'

        if len(descripcion) < 5 or len(descripcion) > 10:
            errores['Descripción'] = 'Debe tener entre 5 y 10 caracteres.'

        if '-' in stock_raw:
            errores['Stock'] = 'No se permite el uso del signo "-".'
        else:
            try:
                stock = int(stock_raw)
                if stock < 1:
                    errores['Stock'] = 'Solo se permiten números positivos mayores a 0.'
            except ValueError:
                errores['Stock'] = 'Debe ser un número válido.'

        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.stock = stock if 'Stock' not in errores else 0

        if not errores:
            try:
                producto.save()
                return redirect('lista_productos')
            except ValidationError as e:
                errores = {k.capitalize(): str(v[0]) for k, v in e.to_dict().items()}

        return render(request, 'app/editar.html', {
            'errores': errores,
            'producto': producto,
            'nombre': nombre,
            'descripcion': descripcion,
            'stock': stock_raw
        })

    return render(request, 'app/editar.html', {
        'errores': {},
        'producto': producto,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'stock': producto.stock
    })

def eliminar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=ObjectId(producto_id))
        producto.delete()
    except Producto.DoesNotExist:
        pass
    return redirect('lista_productos')
