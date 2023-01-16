from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import  PageNumberPagination
from django.shortcuts import get_object_or_404
from .serializers import MovieSerializer, MovieOrderSerializer
from .models import Movie
from users.permissions import IsAdmOrReadOnly, IsAuthenticated

import ipdb

# Create your views here.
class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAdmOrReadOnly]

    def post(self, request: Request) -> Response:        
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, request)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAdmOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, resquest: Request, movie_id: int):
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        

class OrderView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        
        movie_obj = get_object_or_404(Movie, pk=movie_id)

        serializer = MovieOrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie_obj, user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
