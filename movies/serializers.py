from rest_framework import serializers
from .models import Rating, Movie, MovieOrder
from users.serializers import UserSerializer
import ipdb


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, required=False)
    rating = serializers.ChoiceField(
        choices=Rating.choices,
        default=Rating.DEFAULT
    )
    synopsis = serializers.CharField(required=False)
    added_by = serializers.SerializerMethodField()

    def create(self, validated_data):
        movie = Movie.objects.create(**validated_data)

        return movie

    def get_added_by(self, obj):
        return obj.user.email
        

class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = serializers.DateTimeField(read_only=True)
    buyed_by = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_buyed_by(self, obj: MovieOrder):
        return obj.movie.users.all()[0].email

    def get_title(self, obj: MovieOrder):
        return obj.movie.title

    def create(self, validated_data) -> MovieOrder:
        return MovieOrder.objects.create(**validated_data)
    