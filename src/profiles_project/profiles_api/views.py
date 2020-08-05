from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

class HelloApiView(APIView):
    """Test API View"""
    def get(self, request, format=None):
        """Returns a list of api view features"""
        an_apiview=[
        'uses http',
        'django',
        'manually mapped',
        ]
        return Response({'message':'Hello','an_apiview':an_apiview})
