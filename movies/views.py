from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Rating
from .serializers import MovieListSerailizer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, RatingSerializer

class MovieListView(APIView):

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
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

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
        
