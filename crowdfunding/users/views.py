from django.shortcuts import render

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserDetailSerializer

# users/
class CustomUserList(APIView):
    # GET request
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
        
    # POST request
    # TODO Must have unique username and password
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

# users/<pk>     
class CustomUserDetail(APIView):    

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    # GET request       
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    # PUT request
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = self.get_object(pk)
        #if request.user != user or not request.user.is_superuser:
        #    return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        serializer = CustomUserDetailSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE request
    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)        
        user = self.get_object(pk)
        # needs testing
        #if request.user != user.user or not request.user.is_superuser:
        #    return Response(status=status.HTTP_401_UNAUTHORIZED)
        user.delete()
        return Response(
            status=status.HTTP_200_OK        )



