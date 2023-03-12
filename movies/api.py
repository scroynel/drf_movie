# тут будет реализовано views на viewset'ах для актеров

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Actor
from .serializers import (
    ActorSerializer, 
    ActorDetialSerializer,
    )

class ActorViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Actor.objects.all()
        seriallizer = ActorSerializer(queryset, many=True)
        return Response(seriallizer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Actor.objecst.all()
        actor = get_object_or_404(queryset, pk=pk)
        serializer = ActorDetialSerializer(actor)
        return Response(serializer.data)