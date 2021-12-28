from django.contrib.auth import authenticate
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from .models import Client, Good, Status, Project
from .serializers import ClientSerializer, StatusSerializer, ProjectSerializer, GoodSerializer, ProjectPOSTSerializer

# Auth
class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = Client.objects.get(email=request.data.get('email'))
        password = request.data.get('password')
        client = authenticate(username=username, password=password)
        if client:
            return Response({
                "token": client.auth_token.key,
                "is_staff": client.is_staff,
                "id": client.id
            })
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = ()

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Client views
class ClientDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def patch(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Status views
class StatusList(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)

# Good views
class GoodList(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)

# Project views

class ProjectList(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectEdit(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Status.DoesNotExist:
            raise Http404
    
    def patch(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectPOSTSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ProjectPOSTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectClientList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = self.get_object(pk)
        projects = Project.objects.filter(Client=client)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
