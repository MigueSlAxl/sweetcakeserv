# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.core.files import File
# import os
# from django.conf import settings
# import base64


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)







# class User(AbstractBaseUser, PermissionsMixin):
#     first_name = models.CharField(max_length=100, verbose_name='first name')
#     last_name = models.CharField(max_length=100, verbose_name='last name')
#     email = models.EmailField(unique=True, verbose_name='email')
#     password = models.CharField(max_length=100, verbose_name='password')
#     rut = models.CharField(max_length=12, blank=True, null=True, verbose_name='RUT')
#     direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name='direccion')
#     ntelefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de telefono')
#     nemergencia = models.CharField(max_length=15, blank=True, null=True, verbose_name='numero de emergencia')
#     local = models.CharField(max_length=50, blank=True, null=True, verbose_name='local')
#     imagen=models.ImageField(upload_to='accounts/',blank=False,null=True)
#     def imagen_base64(self):
#         if self.imagen and hasattr(self.imagen, 'url'):
#             with self.imagen.open(mode='rb') as f:
#                 img_data = f.read()
#             return base64.b64encode(img_data).decode('utf-8')
#         else:
#             return None
#     def save(self, *args, **kwargs):
#         if not self.imagen:
#             # asigna la imagen por defecto si no se ha proporcionado una imagen
#             img_path = os.path.join(settings.MEDIA_ROOT, 'accounts\default.jpg')
#             with open(img_path, 'rb') as f:
#                 self.imagen.save('accouunts/default.jpg', File(f), save=False)
#         super(User, self).save(*args, **kwargs)
    
    
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     class Meta:
#         ordering = ['id']

#     def __str__(self):
#         return self.email
