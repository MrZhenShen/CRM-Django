from rest_framework import serializers
from .models import Client, Good, Status, Project

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
          'id', 
          'first_name', 
          'last_name', 
          'birth_date', 
          'telephone_number', 
          'email',
          'password',
          'is_staff',
          'company_name',
          'company_link',
          'industry',
          'role',
          'country',
          'city'
        ]

class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = [
          'id',
          'name', 
          'description', 
          'example_image', 
          'pricing'
        ]

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
          'id', 
          'title', 
          'color'
        ]

class ProjectSerializer(serializers.ModelSerializer):
  Good = GoodSerializer()
  Client = ClientSerializer()
  Status = StatusSerializer()

  class Meta:
      model = Project
      fields = [
        'id', 
        'Good', 
        'Client',
        'client_comment',
        'Status'
      ]