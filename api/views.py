from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializar import GenreSerializer, MovieSerializer, UserSerializer, ListSerializer
from .models import Genre, Movie, User, List

# Create your views here.

class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    @action(detail=True, methods=['patch'])
    def add_movie(self, request, pk=None):
        list_instance = self.get_object()
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'detail': 'El campo "movie_id" es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'detail': 'La película especificada no existe.'}, status=status.HTTP_404_NOT_FOUND)
        list_instance.movies.add(movie)
        serializer = self.get_serializer(list_instance)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove_movie(self, request, pk=None):
        list_instance = self.get_object()
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'detail': 'El campo "movie_id" es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'detail': 'La película especificada no existe.'}, status=status.HTTP_404_NOT_FOUND)
        list_instance.movies.remove(movie)
        serializer = self.get_serializer(list_instance)
        return Response(serializer.data)
    
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Autenticación

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            refresh_token = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
                'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'detail': 'Por favor, proporciona el email y la contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'detail': 'Las credenciales son inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh_token = RefreshToken.for_user(user)

        response_data = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token),
            'user': UserSerializer(user).data
        }

        return Response(response_data)
    
class UserUpdateView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtén los nuevos valores de is_staff e is_active del cuerpo de la solicitud
        is_staff = request.data.get("is_staff")
        is_active = request.data.get("is_active")

        # Actualiza los valores si están presentes en la solicitud
        if is_staff is not None:
            user.is_staff = is_staff
        if is_active is not None:
            user.is_active = is_active

        # Guarda los cambios en la base de datos
        user.save()

        return Response({"detail": "Usuario actualizado correctamente."}, status=status.HTTP_200_OK)