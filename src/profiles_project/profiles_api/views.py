from django.shortcuts import render
from .import serializers
from rest_framework import status

# Create your views here.
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from . import models
from .import permissions
from rest_framework.authentication import TokenAuthentication
class HelloApiView(APIView):
    """Test API View"""
    serializer_class=serializers.HelloSerializer
    def get(self, request, format=None):
        """Returns a list of api view features"""
        an_apiview=[
        'uses http',
        'django',
        'manually mapped',
        ]
        return Response({'message':'Hello','an_apiview':an_apiview})
    def post(self,request):
        serializer=serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name=serializer.data.get('name')
            message='Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors,
             status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.UserProfileSerializer
    queryset=models.UserProfile.objects.all()
    authentication_classes=(TokenAuthentication,)
    permission_classes=(permissions.UpdateOwnProfile,)
