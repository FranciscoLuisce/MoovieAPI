from django.contrib import admin
from .models import Genre, Movie, List, User

# Register your models here.

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(List)
admin.site.register(User)