from rest_framework import serializers
from .models import Genre, List, Movie, User

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), source='genre.name')  # Utiliza 'genre.name' como fuente para el campo 'genre', sin cambiar la lista desplegable.

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        genre_name = validated_data.pop('genre')['name']
        genre = Genre.objects.get(name=genre_name)
        movie = Movie.objects.create(genre=genre, **validated_data)
        return movie    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id  # Agrega el campo 'id' a la representación junto con el nombre
        return representation

class ListSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    selected_movies = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=True, write_only=True)

    class Meta:
        model = List
        fields = '__all__'

    def create(self, validated_data):
        movies_data = validated_data.pop('selected_movies', [])
        instance = super().create(validated_data)
        instance.movies.set(movies_data)
        return instance

class UserSerializer(serializers.ModelSerializer):
    lists = serializers.SlugRelatedField(many=True, slug_field='name', queryset=List.objects.all())

    class Meta:
        model = User
        exclude = ['last_login']

