from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'genre', views.GenreViewSet)
router.register(r'movie', views.MovieViewSet)
router.register(r'list', views.ListViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]