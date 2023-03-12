from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .service import get_client_ip, MovieFilter

from .models import Movie, Rating, Actor
from .serializers import MovieListSerailizer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, ActorSerializer, ActorDetialSerializer

# class MovieListView(APIView):

#     def get(self, request):
#         # это поле rating_user будет автоматически добавлено к каждому нашему обьекту movie
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request))),
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')) # F - чтобы можно было производить вычисления
#         )
#         serializer = MovieListSerailizer(movies, many=True)
#         return Response(serializer.data)
    

# тот же класс на generic
# class MovieListView(generics.ListAPIView):

#     serializer_class = MovieListSerailizer
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # это поле rating_user будет автоматически добавлено к каждому нашему обьекту movie
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request))),
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings')) # F - чтобы можно было производить вычисления
#         )
#         return movies


# тот же самый класс только уже через viewsets
# ReadOnlyModelViewSet позволяет делать сразу и get и retrieve
class MovieListView(viewsets.ReadOnlyModelViewSet): 
    filter_beckends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user = models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies
        
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerailizer
        elif self.action == 'retrieve':
            return MovieDetailSerializer

    
# class MovieDetailView(APIView):

#     def get(self, request, pk):
#         movie = Movie.objects.get(pk=pk, draft=False)
#         serailizer = MovieDetailSerializer(movie)
#         return Response(serailizer.data)
    
# тот же класс на generic
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(draft=False) # сам поставить поиск по pk
    serializer_class = MovieDetailSerializer
        
    

# class ReviewCreateView(APIView):

#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)
    
# тот же класс на generic
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    
        

    
# class AddStarRatingView(APIView):

#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)
        
# тот же класс на generic
class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    # при сохранении нам нужно указывать ip
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

        
    
        

# class ActorListView(generics.ListAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorSerializer


# class ActorDetailView(generics.RetrieveAPIView):
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetialSerializer


# то же самое выводим Актеров через viewsets

# class ActorViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Actor.objects.all()
#         serializer = ActorSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = Actor.objects.all()
#         actor = get_object_or_404(queryset, pk=pk)
#         serializer = ActorDetialSerializer(actor)
#         return Response(serializer.data)
    

class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorSerializer
        elif self.action == 'retrieve':
            return ActorDetialSerializer

