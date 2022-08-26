from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, PledgeDetailSerializer
from django.http import Http404
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly

class PledgeList(APIView):
    
    # GET request
    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    # POST request    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # TODO Must not be the project owner
        #if request.user == request.data.project_id:
        #    return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class PledgeDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrReadOnly
    ]

    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk) 
            self.check_object_permissions(self.request, pledge)
            return pledge  
        except Project.DoesNotExist:
            raise Http404
    
    # GET request
    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(pledge)
        return Response(serializer.data)

    # PUT request
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        pledge = self.get_object(pk)
        if request.user != pledge.supporter:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        serializer = PledgeDetailSerializer(
            instance=pledge,
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
        pledge = self.get_object(pk)
        # if request.user != pledge.supporter or not request.user.is_superuser:
        if request.user != pledge.supporter:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        pledge.delete()
        return Response(
            status=status.HTTP_200_OK
        )

# /projects
class ProjectList(APIView):
    # GET request
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    # POST request
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    
    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk) 
            self.check_object_permissions(self.request,project)
            return project  
        except Project.DoesNotExist:
            raise Http404

    # GET request    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    # PUT request
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        project = self.get_object(pk)
        #if request.user != project.owner or not request.user.is_superuser:
        if request.user != project.owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
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
        project = self.get_object(pk)
        # if request.user != project.owner or not request.user.is_superuser:
        if request.user != project.owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        project.delete()
        return Response(
            status=status.HTTP_200_OK
        )
