from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from accounts.models import User,Profile


@csrf_exempt
@api_view(['POST'])
def user_user_add_rest(request, format=None):
    if request.method == 'POST':
        username=request.data['username']
        first_name=request.data['first_name']
        last_name=request.data['last_name']
        email=request.data['email']
        password=request.data['password']
        user_save=User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user_save.save()
        return Response({'Msj':"Usuario Creado"})
    else:
        return Response({'Msj': "Error método no soportado"})
    

@api_view(['GET'])
def user_user_list_rest(request, format=None):
    if request.method == 'GET':
        user_list = User.objects.all()
        user_json = []
        for us in user_list:
            user_json.append({'username':us.username,'first_name':us.first_name,'last_name':us.last_name,'email':us.email})
        return Response({'Users':user_json})
    else:
        return Response({'Msj':"Error método no soportado"})
    
@api_view(['POST'])
def user_user_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            id = request.data['ID']
            username=request.data['username']
            first_name=request.data['first_name']
            last_name=request.data['last_name']
            email=request.data['email']
            password=request.data['password']
            users_array = User.objects.get(pk=id)
            users_array.username=username
            users_array.first_name=first_name
            users_array.last_name=last_name
            users_array.email=email
            users_array.password=password
        except User.DoesNotExist:
            return Response({'No existe'})
        except ValueError:
            return Response({'Dato Invalido'})
    else: 
        return Response({"Error método no soportado"})
    
    # agregar una respuesta de éxito
    return Response({'Actualización exitosa'})


@api_view(['POST'])
def user_user_delete_rest(request, format=None):
    if request.method =='POST':
        try: 
            id = request.data['Eliminar ID']
            if isinstance(id, int):
                productos_array=User.objects.get(pk=id)
                productos_array.delete()
                return Response({'Usuario eliminado con éxito'})
            else:
                return Response({'Ingrese un número entero'})
        except User.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})

