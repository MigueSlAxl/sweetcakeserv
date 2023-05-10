from accounts.models import User, UserStandard
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from knox.auth import AuthToken
from .forms import LoginForm, SignUpForm, editUserForm
from .serializers import RegisterSerializer
from .serializers import UserSerializer
from rest_framework import serializers as serializers
import re
import requests
from datetime import date, datetime
# Create your views here.


def correo_valido(email):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None
#####validador de imagen aun no lo uso
def valid_extension(value):
    if (not value.name.endswith('.png') and
        not value.name.endswith('.jpeg') and
        not value.name.endswith('.bmp') and
            not value.name.endswith('.jpg')) and value.name is not None:
            return Response({'Msj': 'Error, formato no permitido'})
            

@api_view(['POST'])
def user_login_rest(request):
    if request.method == 'POST':
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        _, token = AuthToken.objects.create(user)

        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token
        })

# Endpoint para tomar al usuario al iniciar sesion
@api_view(['GET'])
def get_user_rest(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
            return Response({
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
        else:
            return Response({'error:': 'Usuario no autenticado'})


##Registrar usuario admin
@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    User = serializer.save()

    User.objects.create(
        User=User.id    )

    _, token = AuthToken.objects.create(User)
    print(token)

    return Response({
        'token': token
    })




@api_view(['POST'])
def login_user_rest(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            
            if user.is_client:
                return Response ({'error:': 'Usuario no autenticado'})
            if user.is_admin:
                return redirect('pageadmin')
        else:
            form = LoginForm(request.POST or None)
            msg = None
            if request.method == 'POST':
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    if username == '' or password == '':
                        msg = 'Los campos son requeridos'
                    else:
                        user = authenticate(username=username, password=password)
                        if user is not None and user.is_admin:
                            login(request, user)
                        elif user is not None and user.is_client:
                            login(request, user)
                        else:
                            msg = 'Credenciales invalidas'
                else:
                    msg = 'Error al validar forumulario'
            return Response ({'error:': 'Usuario no autenticado'})



## Logout 
@api_view(['POST'])
def logout_user_rest(request):
    if request.method == 'POST':
        msg = None
        user = request.user
        if user.is_authenticated:
            logout(request)
            msg = 'logout ok'
            messages.add_message(request=request, level=messages.SUCCESS,
                                message="Sesión cerrada correctamente")
        else:
            msg = 'invalid credentials'
        return Response({'msg': msg})




#crear usuario como admin
@api_view(['POST'])
def user_user_add_rest(request, format=None):
    serializer = None
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            userstandard = serializer.save()
            UserStandard.objects.create()
            _, token = AuthToken.objects.create(userstandard)
            print(token , 'dou')
            return Response({
                'token': token,
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def user_user_list_rest(request, format=None):
    if request.method == 'GET':
            userstandard = UserStandard.objects.all()
            serializer = UserSerializer(userstandard, many=True)
            return Response(serializer.data)
    return Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
    



@api_view(['POST'])
def user_user_delete_rest(request, format=None):
    if request.method != 'POST':
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        id = int(request.data['id'])
    except (KeyError, ValueError):
        return Response({'error': 'Ingrese un número entero'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        userstandard_array = UserStandard.objects.get(pk=id)
    except UserStandard.DoesNotExist:
        return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)

    userstandard_array.delete()
    return Response({'detail': 'Usuario eliminado con éxito'})
