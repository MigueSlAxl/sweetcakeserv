from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)

from productos.models import Productos
# Create your views here.

@api_view(['POST'])
def productos_productos_add_rest(request, format=None):
    if request.method == 'POST':
        nombre=request.data['nombre']
        # if nombre=="":
        #     return Response({'Msj':'El nombre no puede ir vacio'})
        fecha_elaboracion=request.data['fecha_elaboracion']
        fecha_vencimiento=request.data['fecha_vencimiento']
        precio=request.data['precio']
        producto_save=Productos(
            nombre=nombre,
            precio=precio,
            fecha_elaboracion=fecha_elaboracion,
            fecha_vencimiento=fecha_vencimiento,
        )
        producto_save.save()
        return Response({'Msj':"Producto Creado"})
    else:
       return Response({'Msj': "Error método no soportado"})
    

@api_view(['GET'])
def productos_productos_list_rest(request, format=None):
    if request.method == 'GET':
        productos_list = Productos.objects.all()
        productos_json = []
        for pr in productos_list:
            productos_json.append({'nombre':pr.nombre,'precio':pr.precio,'fecha_elaboracion':pr.fecha_elaboracion,'fecha_vencimiento':pr.fecha_vencimiento})
        return Response({'List':productos_json})
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def productos_productos_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            producto_id=request.data['ID']
            nombre= request.data['nombre']
            categoria = request.data['categoria']
            precio = request.data['precio']
            fecha_elaboracion = request.data['fecha_elaboracion']
            fecha_vencimiento = request.data['fecha_vencimiento']
            if nombre != '' and categoria!='' and precio!='' and fecha_elaboracion != '' and fecha_vencimiento!='':
                Productos.objects.filter(pk=producto_id).update(nombre=nombre)
                Productos.objects.filter(pk=producto_id).update(categoria=categoria)
                Productos.objects.filter(pk=producto_id).update(precio=precio) 
                Productos.objects.filter(pk=producto_id).update(fecha_elaboracion=fecha_elaboracion)
                Productos.objects.filter(pk=producto_id).update(fecha_vencimiento=fecha_vencimiento)
                producto_json=[]
                producto_array = Productos.objects.get(pk=producto_id)
                producto_json.append({'id':producto_array.id,'nombre':producto_array.nombre,'categoria':producto_array.categoria,'fecha_elaboracion':producto_array.fecha_elaboracion,'fecha_vencimiento': producto_array.fecha_vencimiento,'matricula':producto_array.precio})
                return Response({'Msj':"Datos Actualizados",producto_array.nombre:producto_json}) 
            else:
                return Response({'Msj': "Error los datos no pueden estar en blanco"})
        except Productos.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj':"Metodo no soportado"})



@api_view(['POST'])
def productos_productos_delete_rest(request, format=None):
    if request.method =='POST':
        try: 
            id = request.data['Eliminar ID']
            if isinstance(id, int):
                productos_array=Productos.objects.get(pk=id)
                productos_array.delete()
                return Response({'Producto eliminado con éxito'})
            else:
                return Response({'Ingrese un número entero'})
        except Productos.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})