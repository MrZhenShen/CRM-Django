from django.contrib.auth.models import Permission
from django.shortcuts import render
from django.contrib.auth import authenticate

from .models import Client, Good, Status, Project
from .serializers import ClientSerializer, StatusSerializer, ProjectSerializer, GoodSerializer, ProjectPOSTSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets

# Login

# (<Token: f32ccbd308386ffb816782ffe852f5a982b35268>, True)
# (<Token: d7fe63dae8b18639bd656c1bec3b93b078598e60>, True)

# {
# "email": "admin@mail.com",
# "password": "qwerty"
# ola@mail.com
# 1234
# }

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
class ClientList(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

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

    def delete(self, request, pk, format=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Status views
class StatusList(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)

class StatusDetail(APIView):
    permission_classes = ()

    def get_object(self, pk):
        try:
            return Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        status = self.get_object(pk)
        serializer = StatusSerializer(status)
        return Response(serializer.data)


# Good views
class GoodList(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)

class GoodDetail(APIView):
    permission_classes = ()

    def get_object(self, pk):
        try:
            return Good.objects.get(pk=pk)
        except Good.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        good = self.get_object(pk)
        serializer = GoodSerializer(good)
        return Response(serializer.data)


# Project views

class ProjectList(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ProjectPOSTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientProjectList(APIView):
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

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
