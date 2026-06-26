from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from rest_framework import generics
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by("name")
    serializer_class = ClientSerializer
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all().order_by("name")
    serializer_class = ClientSerializer
