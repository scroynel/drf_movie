from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = format_suffix_patterns([
    path('movie/', views.MovieListView.as_view({'get': 'list'})),
    path('movie/<int:pk>/', views.MovieListView.as_view({'get': 'retrieve'})),
    path('review/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('actors/', views.ActorViewSet.as_view({'get': 'list'})),
    path('actors/<int:pk>', views.ActorViewSet.as_view({'get': 'retrieve'})),
])
