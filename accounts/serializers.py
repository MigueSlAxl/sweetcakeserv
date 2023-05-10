from django.contrib.auth.models import User
from .models import User, UserStandard
from drf_extra_fields.fields import Base64ImageField
import base64
from django.http import JsonResponse
from rest_framework import generics, viewsets, serializers,status, validators


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        imagen=Base64ImageField(required=False)
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name',
                    'is_client', 'is_admin',  'imagen' )

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True,"validators": [validators.UniqueValidator(
            User.objects.all(), "Ya hay un usuario con el email ingresado"
                    )
                ]
            }
        }
        def validate(self, attrs):
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError("Las contraseñas no coinciden")
            return attrs
        

    def create(self, validated_data):
        user = User.objects.first()  # Accediendo al Manager desde una instancia del modelo
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
        user.save()
        print('guardaooo')
        return user

















class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserStandard
        fields = (  'cargo' , 'rut' , 'local' , 'direccion' , 'ntelefono' , 'nemergencia' )
        
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
            
            cargo= validated_data.get('cargo')
            rut= validated_data.get('rut')
            local = validated_data.get('local')
            direccion=validated_data.get('direccion')
            ntelefono=validated_data.get('ntelefono')
            nemergencia=validated_data.get('nemergencia')
                    

            userstandard = UserStandard.objects.create(
                local=local,      
                cargo=cargo,
                rut=rut,
                direccion=direccion,
                ntelefono=ntelefono,
                nemergencia=nemergencia,
            )
            
            print('guardaooo')
            return userstandard

    def get_imagen_base64(self, obj):
        return obj.imagen_base64()










