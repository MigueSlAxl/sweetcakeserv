from io import BytesIO
import base64
from PIL import Image
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User
import os
from django.conf import settings



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'rut', 'direccion', 'ntelefono', 'nemergencia', 'local', 'imagen')


@api_view(['POST'])
def user_user_add_rest(request, format=None):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'rut', 'direccion', 'ntelefono', 'nemergencia', 'local','imagen')
    def get_imagen(self, obj):
        return obj.imagen_base64()

@api_view(['GET'])
def user_user_list_rest(request, format=None):
    if request.method == 'GET':
        usuarios_list = User.objects.all()
        serializer = UsuariosSerializer(usuarios_list, many=True)
        return JsonResponse({'List': serializer.data}, safe=False)
    else:
        return Response({'Msj': "Error método no soportado"})


    
@api_view(['POST'])
def user_user_update_rest(request, format=None):
    if request.method == 'POST':
        try:
            user_id = request.data['ID']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            rut = request.data.get('rut')
            direccion = request.data.get('direccion')
            ntelefono = request.data.get('ntelefono')
            nemergencia = request.data.get('nemergencia')
            local = request.data.get('local')
            imagen=request.data.get('imagen')  # Usar get() para evitar KeyError si la imagen no está presente

            # Si imagen no tiene ningún valor, establecer imagen_data como None y cargar una imagen predeterminada
            if imagen:
                # Procesar la imagen
                data = imagen.split(',', 1)[1]  # Remover el prefijo 'data:image/png;base64,'
                image_data = base64.b64decode(data)
                image = Image.open(ContentFile(image_data))
            else:
                # Si no se proporciona una imagen, establecer imagen_data como None y cargar la imagen predeterminada
                image_path = os.path.join(settings.MEDIA_ROOT, 'accounts/default.jpg')
                with open(image_path, 'rb') as f:
                    image_data = f.read()

            # Buscar al usuario por su ID
            user = User.objects.get(pk=user_id)

            # Actualizar los campos del usuario
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password(password)
            user.rut = rut
            user.direccion = direccion
            user.ntelefono = ntelefono
            user.nemergencia = nemergencia
            user.local = local
            user.imagen.save(f'{user_id}.png', ContentFile(image_data), save=True)

            # Guardar los cambios en la base de datos
            user.save()

            # Crear un diccionario con los datos actualizados del usuario
            updated_user = {
                'ID': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'rut': rut,
                'direccion': direccion,
                'ntelefono': ntelefono,
                'nemergencia': nemergencia,
                'local': local,
                'imagen': imagen,
            }

            # Devolver los datos actualizados del usuario
            return JsonResponse({'user': updated_user})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Método no soportado'}, status=status.HTTP_400_BAD_REQUEST)



@api_view 
def user_user_delete_rest(request, user_id): 
    if request.method =='POST': 
        try: 
            user_id=request.data['user_id']
            if isinstance ( user_id, int):
                user=User.objects.get(pk=user_id)
                user.delete()
                return Response({'Usuario eliminado con éxito'})
            else:
                return Response({'Ingrese un número entero'})
        except User.DoesNotExist:
            return Response({'No existe la ID en la BBDD'})
        except ValueError:
            return Response({'Dato inválido'})
    else: 
        return Response({"Error método no soportado"})