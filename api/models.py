import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


# Create your models here.

class Genre(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Movie(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) # FK
    release_date = models.DateField()

    def __str__(self):
        return self.title

class List(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    movies = models.ManyToManyField(Movie)  # FK Relación ManyToMany con el modelo Movie
    name = models.CharField(max_length=50)
    description  = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        lists = extra_fields.pop('lists', None)  # Obtener las listas del diccionario de campos adicionales
        hashed_password = make_password(password)  # Hashear la contraseña utilizando make_password()
        user = self.model(email=email, name=name, password=hashed_password, **extra_fields)
        user.save(using=self._db)
        
        if lists:
            user.lists.set(lists)  # Asignar las listas utilizando el método set()

        return user
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['secure_password'] = make_password(password)  # Utilizar secure_password
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    profile_photo = models.CharField(max_length=1000)
    lists = models.ManyToManyField(List)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name