from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import FindSH
from .serializers import *
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404

class FindSHList(generics.ListAPIView):
    serializer_class = FindSHListSerializer

    def get_queryset(self):
        queryset = FindSH.objects.all()

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        findshs = FindSH.objects.all()
        serializer = FindSHListSerializer(queryset, many=True, context = {'request': request})

        return Response(serializer.data)

class FindSHCreate(generics.CreateAPIView):
    queryset= FindSH.objects.all()
    serializer_class= FindSHCreateSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = FindSHCreateSerializer(data=request.data, context={'user': user})

        if serializer.is_valid():
            findsh = serializer.save()
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)