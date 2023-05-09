from django.contrib.auth.models import User
from .models import User, UserStandard
from drf_extra_fields.fields import Base64ImageField
import base64
from django.http import JsonResponse
from rest_framework import generics, viewsets, serializers,status, validators


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        imagen=Base64ImageField(required=False)
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',
                    'is_client', 'is_admin',  'imagen' )

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "Ya hay un usuario con el email ingresado"
                    )
                ]
            }
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_client=False,
            is_admin=True
        )
        return user








class UserSerializer(serializers.ModelSerializer):
    imagen_base64 = serializers.SerializerMethodField()

    class Meta:
        model = UserStandard
        fields = ('is_client', 'is_admin', 'nombre' , 'apellido' , 'contraseña' , 'correo' , 'cargo' , 'rut' , 'local' , 'direccion' , 'ntelefono' , 'nemergencia' , 'imagen_base64')
        
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        UserStandard.objects.all(), "Ya hay un usuario con el email ingresado"
                    )
                ]
            }
        }
        
        def create(self, validated_data):
                    
            nombre = validated_data.get('nombre')
            apellido = validated_data.get('apellido')
            contraseña = validated_data.get('contraseña')
            correo = validated_data.get('correo')
            cargo= validated_data.get('cargo')
            rut= validated_data.get('rut')
            local = validated_data.get('local')
            direccion=validated_data.get('direccion')
            ntelefono=validated_data.get('ntelefono')
            nemergencia=validated_data.get('nemergencia')
                    

            userstandard = UserStandard.objects.create(
                local=local,      
                nombre=nombre,
                apellido=apellido,
                cargo=cargo,
                rut=rut,
                direccion=direccion,
                ntelefono=ntelefono,
                nemergencia=nemergencia,
                correo=correo,
                is_client=True,
                is_admin=False
            )
            userstandard.set_password(contraseña)
            userstandard.save()
            return userstandard

    def get_imagen_base64(self, obj):
        return obj.imagen_base64()







