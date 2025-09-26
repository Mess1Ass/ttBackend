from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import CityService
from .serializers import CitySerializer

# Create your views here.


@api_view(["GET"])
def list_cities(request):
    cities = CityService.list_cities()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)
