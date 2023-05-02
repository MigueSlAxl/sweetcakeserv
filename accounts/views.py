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
            user_json.append({'username':us.username,'first_name':us.first_name,'last_name':us.last_name,'email':us.email, 'rut':us.rut,'direccion':us.direccion,'ntelefono':us.ntelefono,'nemergencia':us.nemergencia,'local':us.local})
        return Response({'Users':user_json})
    else:
        return Response({'Msj':"Error método no soportado"})
    
@api_view(['POST'])
def user_user_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            user_id=request.data['ID']
            user_obj = User.objects.get(pk=user_id)
            user_obj.username=request.data['username']
            user_obj.first_name=request.data['first_name']
            user_obj.last_name=request.data['last_name']
            user_obj.email=request.data['email']
            user_obj.password=request.data['password']

            if user_obj.username != '' and user_obj.first_name != '' and user_obj.last_name != '' and user_obj.email != '' and user_obj.password != '':
                user_obj.save()
                user_json=[]
                user_json.append({'id':user_obj.id,'username':user_obj.username,'first_name':user_obj.first_name,'last_name':user_obj.last_name,'email': user_obj.email,'password':user_obj.password, })
                return Response({'Msj':"Datos Actualizados", 'user_data': user_json}) 
            else:
                return Response({'Msj': "Error: los datos no pueden estar en blanco"})
        except User.DoesNotExist:
            return Response({'Msj':"Error: no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})

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