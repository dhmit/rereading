from django.shortcuts import render
from rest_framework import generics
from .models import BabyShoes
from .serializers import BabyShoesSerializer


# Create your views here.
class ListBabyShoes(generics.ListCreateAPIView):
    queryset = BabyShoes.objects.all()
    serializer_class = BabyShoesSerializer


class DetailBabyShoes(generics.RetrieveUpdateDestroyAPIView):
    queryset = BabyShoes.objects.all()
    serializer_class = BabyShoesSerializer
