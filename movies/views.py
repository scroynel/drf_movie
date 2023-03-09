from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from .service import get_client_ip

from .models import Movie, Rating
from .serializers import MovieListSerailizer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer

class MovieListView(APIView):

    def get(self, request):
        # это поле rating_user будет автоматически добавлено к каждому нашему обьекту movie
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request))),
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')) # F - чтобы можно было производить вычисления
        )
        serializer = MovieListSerailizer(movies, many=True)
        return Response(serializer.data)
    
class MovieDetailView(APIView):

    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk, draft=False)
        serailizer = MovieDetailSerializer(movie)
        return Response(serailizer.data)
    

class ReviewCreateView(APIView):

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)
    
class AddStarRatingView(APIView):

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
        
